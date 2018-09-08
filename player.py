#!/usr/local/bin/python3

import logging
import time
import sys

from kazoo.client import KazooClient
from kazoo.recipe.queue import Queue
from numpy import random

class Player:

    def __init__(self):
        logging.basicConfig()
        zk = KazooClient(hosts='127.0.0.1:2181')
        zk.start()
        print('Client begin')
        data = 0
        self.my_queue = Queue(zk, "/queue")

    def post_score(self, score):
        self.my_queue.put('{}:{}'.format(sys.argv[1],str(score)).encode('utf-8'))


def get_normal_random(max_val=1000000):
    mu, sigma = 0, 0.1 # mean and standard deviation
    return int(round(abs(random.normal(mu, sigma, 1) * max_val)))

def main():
    player = Player()
    while True:
        score = get_normal_random()
        delay = get_normal_random(50)
        print('Value set: {}, delay: {}'.format(score, delay))
        player.post_score(score)
        time.sleep(delay)


if __name__ == '__main__':
    main()
