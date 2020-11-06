#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/20 0020 12:10
# @Author  : Hadrianl 
# @File    : main

from ws import IBWS
import os

def main():
    host = os.environ.get('IBHOST')
    port = int(os.environ.get('IBPORT'))
    ibws = IBWS(host, port)
    ibws.run()

if __name__ == '__main__':
    main()