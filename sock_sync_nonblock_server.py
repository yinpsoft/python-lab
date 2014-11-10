#!/usr/bin/env python
# -*- coding: UTF-8 -*-

################################################################################
# Author: billypu - yinpsoft@vip.qq.com
# QQ : 191956428
# Last modified: 2014-11-07 22:03
# Filename: sockserver.py
# Desc:
################################################################################

import sys
import os
import re
import socket
import select
import time

if __name__ == '__main__':
    # init socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(0)
    sock.bind(('', int(sys.argv[1])))
    sock.listen(10)

    # init epoll
    poller = select.epoll()
    poller.register(sock.fileno(), select.EPOLLIN | select.EPOLLOUT)
    
    try:
        connections = {}
        requests = {}
        responses = {}

        while True:
            events = poller.poll(-1)
            print events
            for currfd, event in events:
                print currfd, event
                if currfd == sock.fileno():
                    # in coming connection 
                    print "new connection in coming"
                    newconn, address = sock.accept()
                    newconn.setblocking(0)
                    poller.register(newconn.fileno())

                    connections[newconn.fileno()] = newconn 
                    requests[newconn.fileno()] = b''
                    responses[newconn.fileno()] = b''
                else:
                    if event & select.EPOLLIN:
                        # readable event 
                        requests[currfd] = connections[currfd].recv(1024)
                        print "[{1}] server recv data: {0}".format(requests[currfd], currfd)

                        # todo sth
                        # sim the process timeout
                        time.sleep(float(sys.argv[2]))
                        responses[currfd] = "[{1}] server processed: {0}".format(requests[currfd], currfd)

                        # change interested event
                        poller.modify(currfd, select.EPOLLOUT)

                    elif event & select.EPOLLOUT:
                        # writeable event 
                        sent_len = connections[currfd].sendall(responses[currfd])
                        print "{0} bytes were send back to client".format(sent_len)

                        # change  interested event 
                        poller.modify(currfd, select.EPOLLIN)

                    elif event & select.EPOLLHUP:
                        # closed by peer event 
                        print "[{0}]close connection from client.".format(currfd)
                        connections[currfd].close()
                        del connections[currfd]
                        del requests[currfd]
                        del responses[currfd]
                        poller.unregister(currfd)

    except Exception as e:
        print  "Exception was raised: {0}".format(sys.exc_info())
    finally:
        # TODO:
        print "destroy process"
        poller.unregister(sock.fileno())
        poller.close()
        sock.close()

