#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/20 0020 12:10
# @Author  : Hadrianl 
# @File    : main

from ws import IBWS
import sys

def main():
    host = sys.argv[1]
    port = int(sys.argv[2])
    ibws = IBWS(host, port)
    ibws.run()

if __name__ == '__main__':
    main()