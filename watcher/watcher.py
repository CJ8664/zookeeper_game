#!/usr/local/bin/python3

import logging
import time

from kazoo.recipe.watchers import DataWatch
from kazoo.client import KazooClient
from kazoo.recipe.queue import Queue

zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()
print('Watch begin')
my_queue = Queue(zk, "/queue")

# @zk.DataWatch("/queue")
# def watch_node(data, stat, event):
#     print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))
#     return True

@zk.ChildrenWatch('/queue')
def my_func(children):
    print("Children are %s" % children)

while True:
    time.sleep(0.05)
