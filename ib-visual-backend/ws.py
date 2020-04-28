#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/20 0020 12:26
# @Author  : Hadrianl 
# @File    : ws

from ib_insync import *
import signal
import functools
import websockets
import asyncio
from typing import Set, List, Dict, NamedTuple
from dataclasses import is_dataclass, fields
from collections import defaultdict
import contextlib
import json
import talib
import numpy as np
import datetime as dt
import logging

util.logToConsole()
util.patchAsyncio()
logger = logging.getLogger('ib-visual-backend')
def convert(obj):
    if isinstance(obj, (int, float)) or obj is None:
        return obj
    elif is_dataclass(obj):
        return {field.name: convert(getattr(obj, field.name)) for field in fields(obj)}
    elif isinstance(obj, List):
        return [convert(o) for o in obj]
    elif isinstance(obj, tuple):
        return {k: convert(v) for k, v in zip(obj._fields, obj)}
    else:
        return str(obj)

class IBWS:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.USER: Set[websockets.WebSocketServerProtocol]= set()
        self.BAR2USER: Dict[Set, Set] = defaultdict(set)
        self.TICK2USER: Dict[int, Set] = defaultdict(set)
        self.ib = IB()
        self.bar2ws: Dict[BarDataList, Set] = {}
        self.loop = asyncio.get_event_loop()

    async def register(self, user):
        self.USER.add(user)
        logger.info(f'Register User: {user}')
        if not self.ib.isConnected():
            await self.ib.connectAsync(self.host, self.port, 0)

        await user.send(json.dumps({'t': 'connect_sync'}))

    async def unregiseter(self, user):
        self.USER.remove(user)
        logger.info(f'Unregister User: {user}')
        # TODO: maybe there is a better solution
        for conId, barSize in self.BAR2USER:
            print(conId)
            if user in self.BAR2USER[(conId, barSize)]:
                self.BAR2USER[(conId, barSize)].remove(user)  # remove ws from BAR2USER
                print(self.BAR2USER[(conId, barSize)])
                print(bool(not self.BAR2USER[(conId, barSize)]))

            if not self.BAR2USER[(conId, barSize)]:  # disconnect the send_bar if no ws, for global check cleanup
                print('empty bar')
                for _, bs in self.ib.wrapper.reqId2Subscriber.items():
                    if isinstance(bs, BarDataList) and bs.contract.conId == conId and bs.barSizeSetting == barSize:
                        print("-= send_bar")
                        bs.updateEvent -= self.send_bar

        for conId in self.TICK2USER:
            print(conId)
            if user in self.TICK2USER[conId]:
                self.TICK2USER[conId].remove(user)
                print(self.TICK2USER[conId])
                print(bool(not self.TICK2USER[conId]))
                
            if not self.TICK2USER[conId]:
                print('empty tick')
                for _, t in self.ib.wrapper.reqId2Ticker.items():
                    if t.contract.conId == conId:
                        print("-= send_ticker")
                        t.updateEvent -= self.send_ticker

    async def handle_trade_event(self, event_name):
        event = getattr(self.ib, event_name)

        if not event:
            return

        async for t in event:
            t.log = []
            t = convert(t)
            msg = {'t': 'trade', 'data': t}
            for u in self.USER:
                await u.send(json.dumps(msg))

    async def handle_position_event(self):
        async for p in self.ib.positionEvent:
            pos = p._asdict()
            pos['conId'] = pos.pop('contract').conId
            msg = {'t': 'position', 'data': pos}
            for u in self.USER:
                await u.send(json.dumps(msg))

    async def handle_exec_event(self):
        async for _, fill in self.ib.execDetailsEvent:
            msg = {'t': 'fill', 'data': convert(fill)}
            for u in self.USER:
                await u.send(json.dumps(msg))

    async def send_trades(self, ws):
        trades = self.ib.trades()
        msg = {'t': 'trades', 'data': []}
        for t in trades:
            t.log = []
            t = convert(t)
            msg['data'].append(t)

        await ws.send(json.dumps(msg))

    async def send_positions(self, ws):
        positions = self.ib.positions()
        msg = {'t': 'positions', 'data': []}
        for p in positions:
            pos = p._asdict()
            pos['conId'] = pos.pop('contract').conId
            msg['data'].append(pos)

        await ws.send(json.dumps(msg))

    async def send_contracts(self, contract, ws):
        try:
            contracts = await asyncio.wait_for(self.ib.qualifyContractsAsync(contract), 3)
            for c in contracts:
                await ws.send(json.dumps({'t': 'contract', 'data': c.__dict__}))
        except asyncio.TimeoutError:
            await ws.send(json.dumps({'t': 'error', 'data': '查询合约超时'}))

    async def send_fills(self, ws):
        fills = self.ib.fills()
        msg = {'t': 'fills', 'data': convert(fills)}
        await ws.send(json.dumps(msg))
  
    async def place_order(self, contract, order, ws):
        _ = self.ib.placeOrder(contract, order)

    async def cancel_order(self, order, ws):
        self.ib.cancelOrder(order)

    async def sub_klines(self, contract, barSize, ws):
        print(f'sub_klines:{contract.conId}')
        for _, bs in self.ib.wrapper.reqId2Subscriber.items():
            if isinstance(bs, BarDataList) and bs.contract == contract and bs.barSizeSetting == barSize:
                bars = bs
                break
        else:
            try:
                bars = await asyncio.wait_for(self.ib.reqHistoricalDataAsync(contract, '', '1 D', barSize, 'TRADES', useRTH=False, keepUpToDate=True), 10)
            except asyncio.TimeoutError:
                await ws.send(json.dumps({'error': '订阅K线超时：请确认数据连接是否中断'}))
                return

        conId = bars.contract.conId
        self.BAR2USER[(conId, barSize)].add(ws)
        await ws.send(json.dumps({
            't': 'bars',
            'data': [{'time': str(d.date), 'open': d.open, 'high': d.high, 'low': d.low, 'close': d.close, 'volume': d.volume, 'conId': conId} for d in bars[:]]}))

        if self.send_bar not in bars.updateEvent:
            bars.updateEvent += self.send_bar

    async def unsub_klines(self, contract, barSize, ws):
        conId = contract.conId
        print(f'unsub_klines:{conId}')
        if ws in self.BAR2USER[(conId, barSize)]:
            self.BAR2USER[(conId, barSize)].remove(ws)

    async def sub_ticker(self, contract, ws):
        print(f'sub_ticker:{contract.conId}')
        for _, t in self.ib.wrapper.reqId2Ticker.items():
            if t.contract == contract:
                ticker: Ticker = t
                break
        else:
            try:
                ticker = self.ib.reqMktData(contract)
            except asyncio.TimeoutError:
                await ws.send(json.dumps({'error': '订阅ticker超时：请确认数据连接是否中断'}))
                return

        conId = ticker.contract.conId
        self.TICK2USER[conId].add(ws)
        if self.send_ticker not in ticker.updateEvent:
            ticker.updateEvent += self.send_ticker
    
    async def unsub_ticker(self, contract, ws):
        conId = contract.conId
        print(f'unsub_ticker:{conId}')
        if ws in self.TICK2USER[conId]:
            self.TICK2USER[conId].remove(ws)
   
    async def get_klines(self, contract, _from, _to, ws):
        _to = dt.datetime.fromtimestamp(_to) - dt.timedelta(hours=8)
        _from = dt.datetime.fromtimestamp(_from) - dt.timedelta(hours=8)
        conId = contract.conId
        d = _to - _from

        if d < dt.timedelta(days=1):
            durationStr = f'{d.seconds} S'
        else:
            durationStr = f'{d.days} D'

        try:
            bars = await asyncio.wait_for(self.ib.reqHistoricalDataAsync(contract, _to, durationStr, '1 min', 'TRADES', useRTH=False, keepUpToDate=False), 10)
        except asyncio.TimeoutError:
            await ws.send(json.dumps({'error': '获取K线超时：请确认数据连接是否中断'}))
            return

        await ws.send(json.dumps({
            't': 'bars_',
            'data': [{'time': str(d.date), 'open': d.open, 'high': d.high, 'low': d.low, 'close': d.close, 'volume': d.volume, 'conId': conId} for d in bars[:]]}))
 
    def send_bar(self, bars, hasNewBar):
        d = bars[-1]
        conId = bars.contract.conId
        barSize = bars.barSizeSetting
        for u in self.BAR2USER[(conId, barSize)]:
            self.ib.run(u.send(json.dumps({
                't': 'bar',
                'data': {'time': str(d.date), 'open': d.open, 'high': d.high, 'low': d.low, 'close': d.close, 'volume': d.volume, 'conId': bars.contract.conId}})))

    def send_ticker(self, ticker):
        conId = ticker.contract.conId
        for u in self.TICK2USER[conId]:
            self.ib.run(u.send(json.dumps({
                't': 'ticker',
                'data': {'time': str(ticker.time), 'bid': ticker.bid, 'bidSize': ticker.bidSize, 'ask': ticker.ask, 'askSize': ticker.askSize, 'last': ticker.last, 'lastSize': ticker.lastSize, 'conId': conId}
            })))


    async def place_dynamic_order(self, contract, order: Order, options, ws):
        trigger_type = options['type']
        barSize = options.get('barSize', '1 min')
        lmtOffset = options['lmtOffset']
        triggerOffset = options['triggerOffset']
        period = options['period']
        action = order.action
        # contract.includeExpired = False if contract.includeExpired == 'False' else True

        logger.info(f'Place_dynamic_order: {contract.conId}  {options}')
        if trigger_type == 'MA':
            
            for reqId, bs in self.ib.wrapper.reqId2Subscriber.items():
                if isinstance(bs, BarDataList) and bs.contract == contract and bs.barSizeSetting == barSize :
                    bars = bs
                    break
            else:
                try:       
                    bars = await asyncio.wait_for(self.ib.reqHistoricalDataAsync(contract, '', '1 D', barSize, 'TRADES', useRTH=False, keepUpToDate=True), 10)
                except asyncio.TimeoutError:
                    await ws.send(json.dumps({'t': 'error', 'data': '无法下均线止损单：无法获取合约数据'}))
                    return

            if len(bars) < period:
                await ws.send(json.dumps({'t': 'error', 'data': '无法下均线止损单：合约数据长度不足'}))
                return
            
            # init ma order
            ma = talib.MA(np.array([b.close for b in bars[-period-1:]]), period)
            stopPrice = int(ma[-1])
            triggerOffset = int(triggerOffset)
            if action == 'BUY':
                order.auxPrice = stopPrice + triggerOffset
                order.lmtPrice = order.auxPrice + lmtOffset
            elif action == 'SELL':
                order.auxPrice = stopPrice + triggerOffset
                order.lmtPrice = order.auxPrice - lmtOffset

            order.orderRef = f'{trigger_type}{period}{"+" if triggerOffset>=0 else ""}{triggerOffset}'
            trade = self.ib.placeOrder(contract, order)

            # dynamic_loop

            def dynamic_order(bs, hasNewbar):
                if hasNewbar:
                    if trade.orderStatus.status in ['PendingSubmit', 'ApiPending', 'PreSubmitted']:
                        ma = talib.MA(np.array([b.close for b in bs[-period-1:]]), period)
                        contract = trade.contract
                        order = trade.order
                        stopPrice = int(ma[-1])
                        if action == 'BUY':
                            order.auxPrice = stopPrice + triggerOffset
                            order.lmtPrice = order.auxPrice + lmtOffset
                            self.ib.placeOrder(contract, order)
                        elif action == 'SELL':
                            order.auxPrice = stopPrice + triggerOffset
                            order.lmtPrice = order.auxPrice - lmtOffset
                            self.ib.placeOrder(contract, order)

            bars.updateEvent.connect(dynamic_order)
            trade.filledEvent += lambda t: bars.updateEvent.disconnect(dynamic_order)
            trade.cancelledEvent += lambda t: bars.updateEvent.disconnect(dynamic_order)

    async def disconnect_ib(self, ws):
        self.ib.disconnect()
        self.ib.wrapper.reset()
        self.BAR2USER.clear()
        self.TICK2USER.clear()
        user = list(self.USER)
        for u in user:
            await u.close(1001)

    async def middleware(self, ws, path):
        await self.register(ws)
        try:
            async for message in ws:
                msg = json.loads(message)
                logger.debug(f'Get msg: {message}')
                handler = self.recvMsg2Handler(msg, ws)
                if handler:
                    await handler
        except Exception as e:
            logger.exception(f'middleware error: {e}')
        finally:
            await self.unregiseter(ws)

    def recvMsg2Handler(self, msg, ws):
        if isinstance(msg, Dict) and msg.get('action'):
            if msg['action'] == 'get_all_trades':
                return self.send_trades(ws)
            elif msg['action'] == 'get_all_positions':
                return self.send_positions(ws)
            elif msg['action'] == 'get_all_fills':
                return self.send_fills(ws)    
            elif msg['action'] == 'get_contracts':
                contract = msg.get('data')
                if contract:
                    contract = Contract(**contract)
                    return self.send_contracts(contract, ws)
            elif msg['action'] == 'place_order':
                contract = msg.get('contract')
                order = msg.get('order')
                if contract and order:
                    contract = Contract(**contract)
                    order['softDollarTier'] = SoftDollarTier(**order['softDollarTier'])
                    order = Order(**order)
                    return self.place_order(contract, order, ws)
            elif msg['action'] == 'cancel_order':
                order = msg.get('order')
                if order:
                    order['softDollarTier'] = SoftDollarTier(**order['softDollarTier'])
                    order = Order(**order)
                    return self.cancel_order(order, ws)
            elif msg['action'] == 'place_dynamic_order':
                contract = msg.get('contract')
                order = msg.get('order')
                options = msg.get('options')
                if contract and order and options:
                    contract = Contract(**contract)
                    order['softDollarTier'] = SoftDollarTier(**order['softDollarTier'])
                    order = Order(**order)
                    return self.place_dynamic_order(contract, order, options, ws)
            elif msg['action'] == 'sub_klines':
                contract = msg.get('contract')
                barSize = msg.get('barSize', '1 min')
                if contract:
                    contract = Contract(**contract)
                    return self.sub_klines(contract, barSize, ws)
            elif msg['action'] == 'unsub_klines':
                contract = msg.get('contract')
                barSize = msg.get('barSize', '1 min')
                if contract:
                    contract = Contract(**contract)
                    return self.unsub_klines(contract, barSize, ws)
            elif msg['action'] == 'sub_ticker':
                contract = msg.get('contract')
                if contract:
                    contract = Contract(**contract)
                    return self.sub_ticker(contract, ws)
            elif msg['action'] == 'unsub_ticker':
                contract = msg.get('contract')
                if contract:
                    contract = Contract(**contract)
                    return self.unsub_ticker(contract, ws)
            elif msg['action'] == 'get_klines':
                contract = msg.get('contract')
                _from = msg.get('from')
                _to = msg.get('to')
                if contract and _from and _to:
                    return self.get_klines(contract, _from, _to, ws)
            elif msg['action'] == 'disconnect_ib':
                return self.disconnect_ib(ws)

        
    async def global_check(self): # check if there is no user and no processing event, if so , disconnect
        while True:
            await asyncio.sleep(120)
            print('USER:', self.USER)
            print('BAR2USER:', self.BAR2USER)
            print("TICK2USER:", self.TICK2USER)
            print('bars', [{reqId: sub.updateEvent} for reqId, sub in self.ib.wrapper.reqId2Subscriber.items()])
            if self.USER:  # check if has user
                continue

            close_flag = True

            for _, sub in self.ib.wrapper.reqId2Subscriber.items():  # check if has uncompleted event
                if len(sub.updateEvent):
                    print(sub.updateEvent)
                    close_flag = False

            for _, t in self.ib.wrapper.reqId2Ticker.items():
                if len(t.updateEvent):
                    print(t.updateEvent)
                    close_flag = False
            
            if close_flag:
                self.ib.disconnect()
                self.ib.wrapper.reset()
     
    def run(self):
        server = websockets.serve(self.middleware, '0.0.0.0', 6789)
        self.ib.run(server)
        trade_handlers = [self.handle_trade_event(e) for e in ['openOrderEvent', 'orderStatusEvent']]
        position_handler = self.handle_position_event()
        exec_handler = self.handle_exec_event()
        self.ib.run(*trade_handlers, position_handler, exec_handler, self.global_check())