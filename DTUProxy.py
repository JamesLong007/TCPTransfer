#!/usr/bin/env python
from socket import *
from threading import Thread
import os

socket_list = {}

def main():
    HOST='0.0.0.0'
    PORT=4993
    ADDR=(HOST,PORT)

    tcpSerSock = socket(AF_INET,SOCK_STREAM)
    tcpSerSock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)

    tcpSerSock.bind(ADDR)
    tcpSerSock.listen(5)
    print('server started....')

    while True:
        print("waiting for connection...")
        tcpCliSock,addr = tcpSerSock.accept()

        address = f'{addr[0]}_{addr[1]}'
        socket_list[address] = tcpCliSock

        print(f'connected {address}')

        t = Thread(target=broad_data, args=(tcpCliSock,address,socket_list,))
        t.setDaemon(True)
        t.start()

def broad_data(tcpCliSock,address,socket_list):
    while True:
        data=tcpCliSock.recv(1024)
        if not data:
            break
        print(data)

        sdata = data
        s_list = list(socket_list.keys())
        for key in s_list:
            if key != address:
                try:
                    socket_list[key].send(sdata)
                    print(f'success sent to {key}')
                except Exception:
                    sock_del  = socket_list.pop(key)
                    print(f'failed sent to {key}')
                    sock_del.close()
    #tcpCliSock.close()


if __name__ == '__main__':
    main()