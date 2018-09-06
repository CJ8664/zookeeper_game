#!/usr/local/bin/python3

import logging
import time

from kazoo.client import KazooClient

def consume_trigger(event):
    print('Event captured')

def main():
    zk = KazooClient(hosts='127.0.0.1:2181')
    zk.start()
    print('Client begin')
    zk.ensure_path("/queue")
    data = 0
    while True:
        zk.set("/queue", str(data).encode())
        time.sleep(1)
        print('Value set: {}'.format(data))
        data += 1

if __name__ == '__main__':
    main()
