#!/usr/bin/env python
# -*- coding: UTF-8 -*-

################################################################################
# Author: billypu - yinpsoft@vip.qq.com
# QQ : 191956428
# Last modified: 2014-11-08 23:00
# Filename: sock_sync_nonblock_client.py
# Desc:
################################################################################

import sys
import os
import socket 
import time

if __name__ == '__main__':
    sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock1.connect(('localhost', 9000))
    sock2.connect(('localhost', 9001))
    sock3.connect(('localhost', 9002))

    sock1.setblocking(1)
    sock2.setblocking(1)
    sock3.setblocking(1)

    print time.time()
    sock1.sendall('data from client 1')
    print "data from server 1: {0}, time: {1}".format(sock1.recv(1024), time.time())

    sock2.sendall('data from client 2')
    print "data from server 2: {0}, time: {1}".format(sock2.recv(1024), time.time())

    sock3.sendall('data from client 3')
    print "data from server 3: {0}, time: {1}".format(sock3.recv(1024), time.time())
    print time.time()

    sock1.close()
    sock2.close()
    sock3.close()

