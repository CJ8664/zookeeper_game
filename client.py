#!/usr/local/bin/python3

import logging
import time
import sys

from kazoo.client import KazooClient
from kazoo.recipe.queue import Queue
from numpy import random

logging.basicConfig()
zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()
print('Client begin')
data = 0
my_queue = Queue(zk, "/queue")

mu, sigma = 0, 0.1 # mean and standard deviation

while True:
    data = int(round(abs(random.normal(mu, sigma, 1) * 1000000)))
    my_queue.put((sys.argv[1] + ':' + str(data)).encode('utf-8'))
    time.sleep(1)
    print('Value set: {}'.format(data))
    data += 1

if __name__ == '__main__':
    main()
