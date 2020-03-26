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

util.logToConsole()
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
        self.loop = asyncio.get_event_loop()

    async def register(self, user):
        self.USER.add(user)
        print(f'register:{user}')
        if not self.ib.isConnected():
            print('ib未连接')
            await self.ib.connectAsync(self.host, self.port, 0)
            print('ib已连接')

    async def unregiseter(self, user):
        self.USER.remove(user)
        print(f'unregister:{user}')
        if not self.USER:
            self.ib.disconnect()

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
        self.ib.placeOrder(contract, order)

    async def cancel_order(self, order, ws):
        self.ib.cancelOrder(order)

    async def place_masl_order(self, contract, order: Order, options, ws):
        offset = options['offset']
        period = options['period']
        action = order.action
        init_stop_price = order.auxPrice

        try:
            bars = await asyncio.wait_for(self.ib.reqHistoricalDataAsync(contract, '', f'{(period + 1) * 60} S', '1 min', 'TRADES', useRTH=False, keepUpToDate=True))
        except asyncio.TimeoutError:
            await ws.send(json.dumps({'error': '无法下均线止损单：无法获取合约数据'}))
            return

        trade = self.ib.placeOrder(contract, order)
        async for bs, hasNewbar in bars.updateEvent:
            if hasNewbar and trade.orderStatus.status in ['PendingSubmit', 'ApiPending', 'PreSubmitted']:
                ma = talib.MA(np.array([b.close for b in bs]), period)
                contract = trade.contract
                order = trade.order
                if action == 'BUY':
                    order.auxPrice = ma[0]
                    order.lmtPrice = ma[0] + offset
                    self.ib.placeOrder(contract, order)
                elif action == 'SELL':
                    order.auxPrice = ma[0]
                    order.lmtPrice = ma[0] - offset
                    self.ib.placeOrder(contract, order)


    async def middleware(self, ws, path):
        await self.register(ws)
        try:
            async for message in ws:
                msg = json.loads(message)
                print(f'get msg: {message}')
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
                    print(order)
                    order = Order(**order)
                    return self.cancel_order(order, ws)
            elif msg['action'] == 'place_masl_order':
                contract = msg.get('contract')
                order = msg.get('order')
                options = msg.get('options')
                if contract and order and options:
                    contract.pop('deltaNeutralContract')
                    contract = Contract(**contract)
                    order.pop('softDollarTier')
                    order = Order(**order)
                    return self.place_masl_order(contract, order, options, ws)


    def run(self):
        start_server = websockets.serve(self.middleware, '0.0.0.0', 6789)
        self.ib.run(start_server)
        handlers = [self.handle_trade_event(e) for e in ['openOrderEvent', 'orderStatusEvent']]
        self.ib.run(*handlers)