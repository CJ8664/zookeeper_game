#!/usr/bin/python

import logging
import time
import sys

from kazoo.client import KazooClient
from kazoo.recipe.queue import Queue
from kazoo.recipe.party import Party
from numpy import random

class Player:

    name = ''
    def __init__(self, ip_port, name):
        logging.basicConfig()
        zk = KazooClient(hosts=ip_port)
        zk.start()
        self.name = name
        self.my_queue = Queue(zk, "/csjain_queue")
        self.party = Party(zk, '/csjain_players', self.name)

    def join_party(self):
        self.party.join()

    def leave_party(self):
        self.party.leave()

    def post_score(self, score):
        self.my_queue.put('{}:{}'.format(self.name, str(score)).encode('utf-8'))


def get_normal_random(mu, sigma, max_val=1000000):
    # mean and standard deviation
    return int(round(abs(random.normal(mu, sigma, 1) * max_val)))

def main():

    arg_count = len(sys.argv)
    if arg_count >= 2:
        # IP:PORT
        ip_port = sys.argv[1].split(':')
        if len(ip_port) == 1:
            ip_port = '{}:6000'.format(ip_port[0])
        else:
            ip_port = ip_port[0]
    else:
        print('Zookeeper IP not provided')
        sys.exit(-1)

    if arg_count >= 3:
        # IP:PORT Name
        name = sys.argv[2]
    else:
        print('Player Name missing')
        sys.exit(-1)

    if arg_count >= 4:
        # IP:PORT Name count
        player_turns = int(sys.argv[3])
    else:
        player_turns = float('inf')

    if arg_count >= 5:
        # IP:PORT Name count mean_delay
        u_delay = float(sys.argv[4])
    else:
        u_delay = 0

    if arg_count >= 6:
        # IP:PORT Name count mean_score
        u_score = float(sys.argv[5])
    else:
        u_score = 0.1

    player = Player(ip_port, name)
    print(ip_port, name)
    player.join_party()
    try:
        c = 0
        while c <= player_turns:
            score = get_normal_random(u_delay, u_score)
            delay = get_normal_random(50, u_delay, u_score)
            print('Value set: {}, delay: {}'.format(score, delay))
            player.post_score(score)
            time.sleep(delay)
            c += 1
    except KeyboardInterrupt as ex:
        player.leave_party()

if __name__ == '__main__':
    main()
