#!/usr/local/bin/python

import logging
import time
import sys

from kazoo.client import KazooClient
from kazoo.recipe.queue import Queue
from kazoo.recipe.party import Party
from numpy import random

class Player:

    def __init__(self):
        logging.basicConfig()
        zk = KazooClient(hosts='127.0.0.1:2181')
        zk.start()
        self.my_queue = Queue(zk, "/queue")
        self.party = Party(zk, '/clients', sys.argv[1])

    def join_party(self):
        self.party.join()

    def leave_party(self):
        self.party.leave()

    def post_score(self, score):
        self.my_queue.put('{}:{}'.format(sys.argv[1],str(score)).encode('utf-8'))


def get_normal_random(max_val=1000000):
    mu, sigma = 0, 0.1 # mean and standard deviation
    return int(round(abs(random.normal(mu, sigma, 1) * max_val)))

def main():
    player = Player()
    player.join_party()
    try:
        while True:
            score = get_normal_random()
            delay = get_normal_random(50)
            # print('Value set: {}, delay: {}'.format(score, delay))
            player.post_score(score)
            time.sleep(delay)
    except KeyboardInterrupt as ex:
        player.leave_party()

if __name__ == '__main__':
    main()
