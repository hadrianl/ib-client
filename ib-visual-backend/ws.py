#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/20 0020 12:26
# @Author  : Hadrianl 
# @File    : ws

from ib_insync import *
from asyncio import Queue
import signal
import os
import sys
import functools
import websockets
import asyncio
from typing import Set, List, Dict, NamedTuple, Optional
from dataclasses import is_dataclass, fields
from collections import defaultdict
import contextlib
import json
import talib
import numpy as np
import datetime as dt
from dateutil import parser
import logging

util.logToConsole()
util.patchAsyncio()
logger = logging.getLogger('ib-visual-backend')

def tree(obj):
    """
    Convert object to a tree of lists, dicts and simple values.
    The result can be serialized to JSON.
    """
    if isinstance(obj, (bool, int, float, str, bytes, )):
        return obj
    elif isinstance(obj, (dt.date, dt.time)):
        obj_ = getattr(obj, 'astimezone', None)
        return obj_().isoformat() if obj_ else obj.isoformat()
    elif isinstance(obj, dict):
        return {k: tree(v) for k, v in obj.items()}
    elif util.isnamedtupleinstance(obj):
        return {f: tree(getattr(obj, f)) for f in obj._fields}
    elif isinstance(obj, (list, tuple, set)):
        return [tree(i) for i in obj]
    elif is_dataclass(obj):
        return tree(util.dataclassNonDefaults(obj))
    else:
        return obj if obj is None else str(obj)

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
        self.coroutine_queue = Queue()

    async def register(self, user: websockets.WebSocketServerProtocol):
        self.USER.add(user)
        logger.info(f'Register User: {user}')
        if not self.ib.isConnected():
            await self.ib.connectAsync(self.host, self.port, 0)

        await user.send(json.dumps({'t': 'connect_sync'}))

    async def unregiseter(self, user: websockets.WebSocketServerProtocol):
        self.USER.remove(user)
        logger.info(f'Unregister User: {user}')
        # TODO: maybe there is a better solution
        for conId, barSize in self.BAR2USER:
            if user in self.BAR2USER[(conId, barSize)]:
                self.BAR2USER[(conId, barSize)].remove(user)  # remove ws from BAR2USER

            if not self.BAR2USER[(conId, barSize)]:  # disconnect the send_bar if no ws, for global check cleanup
                for _, bs in self.ib.wrapper.reqId2Subscriber.items():
                    if isinstance(bs, BarDataList) and bs.contract.conId == conId and bs.barSizeSetting == barSize:
                        bs.updateEvent -= self.send_bar

        for conId in self.TICK2USER:
            if user in self.TICK2USER[conId]:
                self.TICK2USER[conId].remove(user)
                
            if not self.TICK2USER[conId]:
                for _, t in self.ib.wrapper.reqId2Ticker.items():
                    if t.contract.conId == conId:
                        t.updateEvent -= self.send_ticker

    async def handle_coroutines(self):
        while True:
            c = await self.coroutine_queue.get() # get coroutine(send_bar or send_ticker) from queue 
            await c
    
    async def handle_account_event(self):
        msg = {'t': 'account_value', 'data': None}
        async for a in self.ib.accountValueEvent.merge(self.ib.accountSummaryEvent):
            msg['data'] = tree(a)
            msg_json = json.dumps(msg)
            for u in self.USER:
                await u.send(msg_json)

    async def handle_trade_event(self, event_name: str):
        event = getattr(self.ib, event_name)
        msg = {'t': 'trade', 'data': None}
        async for t in event:
            t.log = []
            # t.fills = []
            msg['data'] = tree(t)
            msg_json = json.dumps(msg)
            for u in self.USER:
                await u.send(msg_json)

    async def handle_position_event(self):
        msg = {'t': 'position', 'data': None}
        async for p in self.ib.positionEvent:
            msg['data'] = tree(p)
            msg_json = json.dumps(msg)
            for u in self.USER:
                await u.send(msg_json)
    
    async def handle_portfolioItem_event(self):
        msg = {'t': 'portfolioItem', 'data': None}
        async for p in self.ib.updatePortfolioEvent:
            msg['data'] = tree(p)
            msg_json = json.dumps(msg)
            for u in self.USER:
                await u.send(msg_json)

    async def handle_exec_event(self):
        msg = {'t': 'fill', 'data': None}
        async for _, fill in self.ib.execDetailsEvent:
            msg['data'] = tree(fill)
            msg_json = json.dumps(msg)
            for u in self.USER:
                await u.send(msg_json)

    async def send_trades(self, ws: websockets.WebSocketServerProtocol):
        trades = self.ib.trades()
        msg = {'t': 'trades', 'data': []}
        for t in trades:
            t.log = []
            # t.fills = []
            msg['data'].append(tree(t))

        await ws.send(json.dumps(msg))

    async def send_positions(self, ws: websockets.WebSocketServerProtocol):
        positions = self.ib.positions()
        msg = {'t': 'positions', 'data': tree(positions)}

        await ws.send(json.dumps(msg))

    async def send_portfolio(self, ws: websockets.WebSocketServerProtocol):
        portfolio = self.ib.portfolio()
        msg = {'t': 'portfolio', 'data': tree(portfolio)}

        await ws.send(json.dumps(msg))

    async def send_contracts(self, contract: Contract, ws: websockets.WebSocketServerProtocol):
        try:
            contracts = await asyncio.wait_for(self.ib.qualifyContractsAsync(contract), 3)
            for c in contracts:
                await ws.send(json.dumps({'t': 'contract', 'data': tree(c)}))
        except asyncio.TimeoutError:
            await ws.send(json.dumps({'t': 'error', 'data': '查询合约超时'}))

    async def send_fills(self, ws: websockets.WebSocketServerProtocol):
        fills = self.ib.fills()
        msg = {'t': 'fills', 'data': tree(fills)}

        await ws.send(json.dumps(msg))

    async def send_account_values(self, ws: websockets.WebSocketServerProtocol):
        accValues = self.ib.accountValues()
        msg = {'t': 'account_values', 'data': tree(accValues)}

        await ws.send(json.dumps(msg))
  
    async def place_order(self, contract: Contract, order: Order, ws: websockets.WebSocketServerProtocol):
        _ = self.ib.placeOrder(contract, order)

    async def place_bracket_orders(self, contract: Contract, orderParam: Dict, ws: websockets.WebSocketServerProtocol):
        orders = self.ib.bracketOrder(**orderParam)
        for o in orders:
            _ = self.ib.placeOrder(contract, o)

    async def cancel_order(self, order, ws):
        self.ib.cancelOrder(order)

    async def sub_klines(self, contract: Contract, barSize: str, ws: websockets.WebSocketServerProtocol):
        # logger.info(f'sub_klines:{contract.conId}')
        for _, bs in self.ib.wrapper.reqId2Subscriber.items():
            if isinstance(bs, BarDataList) and bs.contract == contract and bs.barSizeSetting == barSize:
                bars = bs
                break
        else:
            try:
                if not contract.exchange: # contract in position or portfolio has no exchange
                    contract.exchange = "HKFE"
                bars = await asyncio.wait_for(self.ib.reqHistoricalDataAsync(contract, '', '2 D', barSize, 'TRADES', useRTH=False, keepUpToDate=True), 10)
            except asyncio.TimeoutError:
                await ws.send(json.dumps({'t':'error', 'data': '订阅K线超时：请确认数据连接是否中断'}))
                return

        conId = bars.contract.conId
        self.BAR2USER[(conId, barSize)].add(ws)
        await ws.send(json.dumps({
            't': 'bars',
            'data': [{'time': str(d.date), 'open': d.open, 'high': d.high, 'low': d.low, 'close': d.close, 'volume': d.volume, 'conId': conId} for d in bars[:]]}))

        if self.send_bar not in bars.updateEvent:
            bars.updateEvent += self.send_bar

    async def unsub_klines(self, contract: Contract, barSize: str, ws: websockets.WebSocketServerProtocol):
        conId = contract.conId
        if ws in self.BAR2USER[(conId, barSize)]:
            self.BAR2USER[(conId, barSize)].remove(ws)

    async def sub_ticker(self, contract: Contract, ws: websockets.WebSocketServerProtocol):
        for _, t in self.ib.wrapper.reqId2Ticker.items():
            if t.contract == contract:
                ticker: Ticker = t
                break
        else:
            try:
                if not contract.exchange: # contract in position or portfolio has no exchange
                    contract.exchange = "HKFE"
                ticker = self.ib.reqMktData(contract)
            except asyncio.TimeoutError:
                await ws.send(json.dumps({'t':'error', 'data': '订阅ticker超时：请确认数据连接是否中断'}))
                return

        conId = ticker.contract.conId
        self.TICK2USER[conId].add(ws)
        if self.send_ticker not in ticker.updateEvent:
            ticker.updateEvent += self.send_ticker
    
    async def unsub_ticker(self, contract: Contract, ws: websockets.WebSocketServerProtocol):
        conId = contract.conId
        if ws in self.TICK2USER[conId]:
            self.TICK2USER[conId].remove(ws)
   
    async def get_klines(self, contract: Contract, end: str, barSize: str, duration: str, ws: websockets.WebSocketServerProtocol):
        conId = contract.conId
        end = parser.parse(end)

        try:
            bars = await asyncio.wait_for(self.ib.reqHistoricalDataAsync(contract, end, duration, barSize, 'TRADES', useRTH=False, keepUpToDate=False), 10)
        except asyncio.TimeoutError:
            await ws.send(json.dumps({'t':'error', 'data': '获取K线超时：请确认数据连接是否中断'}))
            return

        await ws.send(json.dumps({
            't': 'bars_',
            'data': [{'time': str(d.date), 'open': d.open, 'high': d.high, 'low': d.low, 'close': d.close, 'volume': d.volume, 'conId': conId} for d in bars[:]]}))

    def send_bar(self, bars: BarDataList, hasNewBar: bool):
        d = bars[-1]
        conId = bars.contract.conId
        barSize = bars.barSizeSetting
        msg_json = json.dumps({
            't': 'bar',
            'data': {'time': str(d.date), 'open': d.open, 'high': d.high, 'low': d.low, 'close': d.close, 'volume': d.volume, 'conId': bars.contract.conId}})
        for u in self.BAR2USER[(conId, barSize)]:
            self.coroutine_queue.put_nowait(u.send(msg_json))

    def send_ticker(self, ticker: Ticker):
        conId = ticker.contract.conId
        msg_json = json.dumps({
                    't': 'ticker', 
                    'data': {'time': ticker.time.astimezone().isoformat(), 'bid': ticker.bid, 'bidSize': ticker.bidSize, 'ask': ticker.ask, 'askSize': ticker.askSize, 'last': ticker.last, 'lastSize': ticker.lastSize, 'conId': conId}
                    })
        for u in self.TICK2USER[conId]:
            self.coroutine_queue.put_nowait(u.send(msg_json))

    async def place_dynamic_order(self, contract, order: Order, options: Dict, ws: websockets.WebSocketServerProtocol):
        trigger_type = options['type']
        barSize = options.get('barSize', '1 min')
        lmtOffset = options['lmtOffset']
        triggerOffset = options['triggerOffset']
        period = options['period']
        action = order.action

        logger.info(f'Place_dynamic_order: {contract.conId}  {options}')
        if trigger_type == 'MA':
            
            for _, bs in self.ib.wrapper.reqId2Subscriber.items():
                if isinstance(bs, BarDataList) and bs.contract == contract and bs.barSizeSetting == barSize :
                    bars = bs
                    break
            else:
                try:       
                    bars = await asyncio.wait_for(self.ib.reqHistoricalDataAsync(contract, '', '2 D', barSize, 'TRADES', useRTH=False, keepUpToDate=True), 10)
                except asyncio.TimeoutError:
                    await ws.send(json.dumps({'t': 'error', 'data': '无法下均线止损单：无法获取合约数据'}))
                    return

            if len(bars) < period:
                await ws.send(json.dumps({'t': 'error', 'data': '无法下均线止损单：合约数据长度不足'}))
                return
            
            # init ma order
            ma = talib.MA(np.array([b.close for b in bars[-period-1:]]), period)
            currentClose = bars[-1].close
            stopPrice = int(ma[-1])
            triggerOffset = int(triggerOffset)
            
            if action == 'BUY':
                order.auxPrice = stopPrice + triggerOffset
                order.lmtPrice = order.auxPrice + lmtOffset
                if currentClose < stopPrice:
                    order.orderType = 'STP LMT'
                else:
                    order.orderType = 'LIT'
            elif action == 'SELL':
                order.auxPrice = stopPrice + triggerOffset
                order.lmtPrice = order.auxPrice - lmtOffset
                if currentClose > stopPrice:
                    order.orderType = 'STP LMT'
                else:
                    order.orderType = 'LIT'

            order.orderRef = f'{trigger_type}{period}{"+" if triggerOffset>=0 else "-"}{triggerOffset}@{barSize}'
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

    async def cancel_all(self, ws: websockets.WebSocketServerProtocol):
        logger.info(f'{ws} request cancel all')
        self.ib.reqGlobalCancel()
    
    async def disconnect_ib(self, ws: websockets.WebSocketServerProtocol):
        self.ib.disconnect()
        self.ib.wrapper.reset()
        self.BAR2USER.clear()
        self.TICK2USER.clear()
        user = list(self.USER)
        for u in user:
            await u.close(1001)

    async def middleware(self, ws: websockets.WebSocketServerProtocol, path: str):
        await self.register(ws)
        try:
            async for message in ws:
                msg = json.loads(message)
                logger.debug(f'Get msg: {message}')
                handler = self.recvMsg2Handler(msg, ws)
                if handler:
                    fut = asyncio.ensure_future(handler)
                    await fut
        except Exception as e:
            logger.exception(f'middleware error: {e}')
        finally:
            await self.unregiseter(ws)

    def recvMsg2Handler(self, msg: Dict, ws: websockets.WebSocketServerProtocol):
        if isinstance(msg, Dict) and msg.get('action'):
            # TODO: try dict, long ugly control flow
            action = msg['action']
            if action == 'get_all_trades':
                return self.send_trades(ws)
            elif action == 'get_all_positions':
                return self.send_positions(ws)
            elif action == 'get_all_portfolio':
                return self.send_portfolio(ws)
            elif action == 'get_all_fills':
                return self.send_fills(ws)    
            elif action == 'get_contracts':
                contract = msg.get('data')
                if contract:
                    contract = Contract(**contract)
                    return self.send_contracts(contract, ws)
            elif action == 'get_all_account_values':
                return self.send_account_values(ws)
            elif action == 'place_order':
                contract = msg.get('contract')
                order = msg.get('order')
                if contract and order:
                    contract = Contract(**contract)
                    order['softDollarTier'] = SoftDollarTier(**order['softDollarTier'])
                    order = Order(**order)
                    return self.place_order(contract, order, ws)
            elif action == 'place_bracket_orders':
                orderParam = msg.get('orderParam')
                contract = msg.get('contract')
                if contract and orderParam:
                    contract = Contract(**contract)
                    return self.place_bracket_orders(contract, orderParam, ws)  
            elif action == 'cancel_order':
                order = msg.get('order')
                if order:
                    order['softDollarTier'] = SoftDollarTier(**order['softDollarTier'])
                    order = Order(**order)
                    return self.cancel_order(order, ws)
            elif action == 'place_dynamic_order':
                contract = msg.get('contract')
                order = msg.get('order')
                options = msg.get('options')
                if contract and order and options:
                    contract = Contract(**contract)
                    order['softDollarTier'] = SoftDollarTier(**order['softDollarTier'])
                    order = Order(**order)
                    return self.place_dynamic_order(contract, order, options, ws)
            elif action == 'sub_klines':
                contract = msg.get('contract')
                barSize = msg.get('barSize', '1 min')
                if contract:
                    contract = Contract(**contract)
                    return self.sub_klines(contract, barSize, ws)
            elif action == 'unsub_klines':
                contract = msg.get('contract')
                barSize = msg.get('barSize', '1 min')
                if contract:
                    contract = Contract(**contract)
                    return self.unsub_klines(contract, barSize, ws)
            elif action == 'sub_ticker':
                contract = msg.get('contract')
                if contract:
                    contract = Contract(**contract)
                    return self.sub_ticker(contract, ws)
            elif action == 'unsub_ticker':
                contract = msg.get('contract')
                if contract:
                    contract = Contract(**contract)
                    return self.unsub_ticker(contract, ws)
            elif action == 'get_klines':
                contract = msg.get('contract')
                duration = msg.get('duration', '1 D')
                end = msg.get('end')
                barSize = msg.get('barSize', '1 min')
                if contract and end:
                    contract = Contract(**contract)
                    return self.get_klines(contract, end, barSize, duration, ws)
            elif action == 'cancel_all':
                return self.cancel_all(ws)
            elif action == 'disconnect_ib':
                return self.disconnect_ib(ws)
      
    async def global_check(self): # check if there is no user and no processing event, if so , disconnect
        while True:
            await asyncio.sleep(300)
            if self.USER:  # check if has user
                continue

            close_flag = True

            for _, sub in self.ib.wrapper.reqId2Subscriber.items():  # check if has uncompleted event
                if len(sub.updateEvent):
                    close_flag = False

            for _, t in self.ib.wrapper.reqId2Ticker.items():
                if len(t.updateEvent):
                    close_flag = False
            
            if close_flag:
                self.ib.disconnect()
                self.ib.wrapper.reset()

    def handle_sigterm(self):
        self.loop.stop()
     
    def run(self):
        server = websockets.serve(self.middleware, '0.0.0.0', 6789)
        self.ib.run(server)
        trade_handlers = [self.handle_trade_event(e) for e in ['openOrderEvent', 'orderStatusEvent']]
        account_handler = self.handle_account_event()
        position_handler = self.handle_position_event()
        portfolioItem_handler = self.handle_portfolioItem_event()
        exec_handler = self.handle_exec_event()
        coroutine_handler = self.handle_coroutines()
        global_check = self.global_check()

        # receive sigterm from docker to stop the loop
        if sys.platform == 'win32': # windows not support add_signal_handler
            signal.signal(signal.SIGTERM, signal.SIG_DFL)
        else:
            self.loop.add_signal_handler(signal.SIGTERM, self.handle_sigterm)
            
        self.ib.run(coroutine_handler, *trade_handlers, position_handler, portfolioItem_handler, exec_handler, account_handler, global_check)