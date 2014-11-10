#!/usr/bin/env python
# -*- coding: UTF-8 -*-

################################################################################
# Author: billypu - yinpsoft@vip.qq.com
# QQ : 191956428
# Last modified: 2014-11-07 23:09
# Filename: sockclient.py
# Desc:
################################################################################

import sys
import os
import time
import socket
import select


# noinspection PyBroadException
class Connector:
    """
    客户端连接类
    """
    def __init__(self, ip, port, blocking=False):
        '''

        :param ip:
        :param port:
        :param blocking:
        :return:
        '''
        self.serverIp = ip
        self.serverPort = port
        self.blocking = blocking
        self.requestbuf = b''
        self.responsebuf = b''
        self.sockObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        '''

        :return:
        '''
        try:
            self.sockObj.connect((self.serverIp, self.serverPort))
            self.sockObj.setblocking(self.blocking)
        except:
            print sys.exc_info()
        finally:
            pass

    def fileno(self):
        return self.sockObj.fileno()

    def setdata(self, data):
        self.requestbuf = data

    def remote_ip(self):
        return self.serverIp

    def remote_port(self):
        return self.serverPort

    def remote_addr(self):
        return (self.serverIp, self.serverPort)

    def send(self, buffer = None):
        try:
            if buffer == None:
                self.sockObj.sendall(self.requestbuf)
            else:
                self.sockObj.sendall(buffer)
        except:
            print sys.exc_info()
        finally:
            pass

    def recv(self, len = 1024):
        try:
            self.responsebuf = self.sockObj.recv(len)
        except:
            print sys.exc_info()
        finally:
            pass

    def close(self):
        self.sockObj.close()

class EPollUnit:
    '''

    '''
    def __init__(self):
        pass

    def add(self, connector):
        pass

    def mod(self, fd, event):
        pass

    def remove(self, fd):
        pass

    def poll(self, timeout):
        pass


class ConnectionManager:
    def __init__(self, pollunit):
        pass

if __name__ == '__main__':

    try:
        poller = select.epoll()

        c1 = Connector('localhost', 9000)
        c2 = Connector('localhost', 9001)
        c3 = Connector('localhost', 9002)

        c1.connect()
        c2.connect()
        c3.connect()

        poller.register(c1.fileno())
        poller.register(c2.fileno())
        poller.register(c3.fileno())

        connections = {}
        answered = {}

        connections[c1.fileno()] = c1
        connections[c2.fileno()] = c2
        connections[c3.fileno()] = c3

        answered[c1.fileno()] = False
        answered[c2.fileno()] = False
        answered[c3.fileno()] = False
        ans = 0

        c3.send('data from sock client 3')
        c2.send('data from socket client 2')
        c1.send('data from socket client 1')

        while True and ans < 3:
            events = poller.poll(-1)
            for fileno, event in events:
                if event & select.EPOLLIN:
                    print "event[{0}] fd[{1}]".format(event, fileno)
                    print "[{2}] data from server port {0}: {1}".format(connections[fileno], connections[fileno].recv(1024), time.time())
                    if answered[fileno] == False:
                        answered[fileno] = True
                        ans = ans + 1

        raw_input()

        c1.close()
        c2.close()
        c3.close()
    except:
        print sys.exc_info()
        print sys.exc_traceback
        print sys.exc_value

    finally:
        pass