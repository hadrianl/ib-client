#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/20 0020 12:26
# @Author  : Hadrianl 
# @File    : ws

from ib_insync import *
import websockets
import asyncio
from typing import Set, List, Dict
from dataclasses import is_dataclass, fields
import contextlib
import json
import talib
import numpy as np
import logging

util.logToConsole()
logger = logging.getLogger('ib-visual-backend')
def convert(obj):
    if is_dataclass(obj):
        return {field.name: convert(getattr(obj, field.name)) for field in fields(obj)}
    elif isinstance(obj, List):
        return [convert(o) for o in obj]
    else:
        return str(obj)

class IBWS:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.USER: Set[websockets.WebSocketServerProtocol]= set()
        self.ib = IB()
        self.bars2Semaphore: Dict[BarDataList, int] = {}
        self.loop = asyncio.get_event_loop()

    async def register(self, user):
        self.USER.add(user)
        logger.info(f'Register User: {user}')
        if not self.ib.isConnected():
            await self.ib.connectAsync(self.host, self.port, 0)

    async def unregiseter(self, user):
        self.USER.remove(user)
        logger.info(f'Unregister User: {user}')
        # if not self.USER:
        #     self.ib.disconnect()

    async def handle_trade_event(self, event_name):
        event = getattr(self.ib, event_name)

        if not event:
            return

        async for t in event:
            t.log = []
            t = convert(t)
            msg = {'trade': t}
            for u in self.USER:
                await u.send(json.dumps(msg))

    async def send_trades(self, ws):
        trades = self.ib.trades()
        msg = {'trades': []}
        for t in trades:
            t.log = []
            t = convert(t)
            msg['trades'].append(t)

        await ws.send(json.dumps(msg))

    async def send_contracts(self, contract, ws):
        try:
            contracts = await asyncio.wait_for(self.ib.qualifyContractsAsync(contract), 3)
            for c in contracts:
                await ws.send(json.dumps({'contract': convert(c)}))
        except asyncio.TimeoutError:
            await ws.send(json.dumps({'error': '查询合约超时'}))
   
    async def place_order(self, contract, order, ws):
        trade = self.ib.placeOrder(contract, order)

    async def cancel_order(self, order, ws):
        order.orderId = int(order.orderId)
        order.permId = int(order.permId)
        order.clientId = int(order.clientId)
        self.ib.cancelOrder(order)

    async def place_dynamic_order(self, contract, order: Order, options, ws):
        trigger_type = options['type']
        offset = options['offset']
        period = options['period']
        action = order.action
        contract.includeExpired = False if contract.includeExpired == 'False' else True

        logger.info(f'Place_dynamic_order: {contract.conId}  {options}')
        if trigger_type == 'MA':
            try:
                for bs in self.bars2Semaphore:
                    if bs.contract.conId == int(contract.conId):
                        bars = bs
                        break
                else:
                    bars = await asyncio.wait_for(self.ib.reqHistoricalDataAsync(contract, '', '1 D', '1 min', 'TRADES', useRTH=False, keepUpToDate=True), 10)
                    self.bars2Semaphore[bars] = 0
            except asyncio.TimeoutError:
                await ws.send(json.dumps({'error': '无法下均线止损单：无法获取合约数据'}))
                return
            
            # init ma order
            ma = talib.MA(np.array([b.close for b in bars[-period-1:]]), period)
            stopPrice = int(ma[-1])
            if action == 'BUY':
                order.auxPrice = stopPrice
                order.lmtPrice = stopPrice + offset
            elif action == 'SELL':
                order.auxPrice = stopPrice
                order.lmtPrice = stopPrice - offset

            order.orderRef = f'{trigger_type}{period}'
            trade = self.ib.placeOrder(contract, order)

            # dynamic_loop
            self.bars2Semaphore[bars] += 1

            def dynamic_order(bs, hasNewbar):
                if hasNewbar:
                    if trade.orderStatus.status in ['PendingSubmit', 'ApiPending', 'PreSubmitted']:
                        ma = talib.MA(np.array([b.close for b in bs[-period-1:]]), period)
                        contract = trade.contract
                        order = trade.order
                        stopPrice = int(ma[-1])
                        if action == 'BUY':
                            order.auxPrice = stopPrice
                            order.lmtPrice = stopPrice + offset
                            self.ib.placeOrder(contract, order)
                        elif action == 'SELL':
                            order.auxPrice = stopPrice
                            order.lmtPrice = stopPrice - offset
                            self.ib.placeOrder(contract, order)

            bars.updateEvent.connect(dynamic_order)
            trade.filledEvent += lambda t: bars.updateEvent.disconnect(dynamic_order)
            trade.cancelledEvent += lambda t: bars.updateEvent.disconnect(dynamic_order)


    async def middleware(self, ws, path):
        await self.register(ws)
        try:
            async for message in ws:
                msg = json.loads(message)
                logger.debug(f'Get msg: {message}')
                handler = self.recvMsg2Handler(msg, ws)
                if handler:
                    await handler
        finally:
            await self.unregiseter(ws)

    def recvMsg2Handler(self, msg, ws):
        if isinstance(msg, Dict) and msg.get('action'):
            if msg['action'] == 'get_all_trades':
                return self.send_trades(ws)
            elif msg['action'] == 'get_contracts':
                contract = msg.get('data')
                if contract:
                    contract = Contract(**contract)
                    return self.send_contracts(contract, ws)
            elif msg['action'] == 'place_order':
                contract = msg.get('contract')
                order = msg.get('order')
                if contract and order:
                    contract.pop('deltaNeutralContract')
                    contract = Contract(**contract)
                    order.pop('softDollarTier')
                    order = Order(**order)
                    return self.place_order(contract, order, ws)
            elif msg['action'] == 'cancel_order':
                order = msg.get('order')
                if order:
                    order.pop('softDollarTier')
                    order = Order(**order)
                    return self.cancel_order(order, ws)
            elif msg['action'] == 'place_dynamic_order':
                contract = msg.get('contract')
                order = msg.get('order')
                options = msg.get('options')
                if contract and order and options:
                    contract.pop('deltaNeutralContract')
                    contract = Contract(**contract)
                    order.pop('softDollarTier')
                    order = Order(**order)
                    return self.place_dynamic_order(contract, order, options, ws)

    def run(self):
        start_server = websockets.serve(self.middleware, '0.0.0.0', 6789)
        self.ib.run(start_server)
        handlers = [self.handle_trade_event(e) for e in ['openOrderEvent', 'orderStatusEvent']]
        self.ib.run(*handlers)