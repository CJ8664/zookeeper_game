#!/usr/local/bin/python3

import logging
import time

from kazoo.recipe.watchers import DataWatch
from kazoo.client import KazooClient

zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()
print('Watch begin')
zk.ensure_path("/queue")

@zk.DataWatch("/queue")
def watch_node(data, stat, event):
    print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))
    return True

while True:
    time.sleep(5)
