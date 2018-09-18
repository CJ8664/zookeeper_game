#!/usr/bin/python

import logging
import sys
import time

from kazoo.client import KazooClient
from kazoo.recipe.queue import Queue
from kazoo.recipe.party import Party
from numpy import random

class Player:

    name = ''

    def __init__(self, ip_port, name):
        '''Initialize everyting for the player'''
        self.name = name
        logging.basicConfig()

        # Create client
        self.zk = KazooClient(hosts=ip_port, logger=logging)
        self.zk.start()

        # Ensure Paths
        self.zk.ensure_path('/csjain_queue')
        self.zk.ensure_path('/csjain_players')

        # Create Data structures
        self.my_queue = Queue(self.zk, '/csjain_queue')
        self.party = Party(self.zk, '/csjain_players', self.name)

    def join_party(self):
        '''Add player to list of current online players'''
        self.party.join()

    def leave_party(self):
        '''Remove player from list of current online players'''
        self.party.leave()

    def post_score(self, score):
        '''Post a random score'''
        self.my_queue.put('{}:{}'.format(self.name, str(score)).encode('utf-8'))


def get_normal_random(mu, var):
    '''Helper method to generate random number
    given the mean and standard deviation=1.5'''
    return int(abs(random.normal(mu, var*mu, 1)))

def main():

    arg_count = len(sys.argv)
    if arg_count >= 2:
        # IP:PORT
        ip_port = sys.argv[1].split(':')
        if len(ip_port) == 1:
            ip_port = '{}:6000'.format(ip_port[0])
        else:
            ip_port = sys.argv[1]
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
        player_turns = -1

    if arg_count >= 5:
        # IP:PORT Name count mean_delay
        u_delay = float(sys.argv[4])
    else:
        u_delay = 4

    if arg_count >= 6:
        # IP:PORT Name count mean_score
        u_score = float(sys.argv[5])
    else:
        u_score = 4

    player = Player(ip_port, name)
    print('Starting Player at {} with name {}'.format(ip_port, name))
    if name in set(player.party):
        print('Player {} is already online, exiting...'.format(name))
        sys.exit(0)
    player.join_party()

    try:
        if player_turns == -1: # Manual mode
            while True:
                print('Enter Score: '),
                score = int(raw_input())
                print('Score published: {}'.format(score))
                player.post_score(score)
        else: # Batch Mode
            c = 0
            while c <= player_turns:
                score = get_normal_random(u_delay, 0.1)
                delay = get_normal_random(u_score, 0.35)
                print('Score published: {}, delay: {}'.format(score, delay))
                player.post_score(score)
                time.sleep(delay)
                c += 1
            player.leave_party()
    except KeyboardInterrupt as ex:
        player.leave_party()

if __name__ == '__main__':
    main()
