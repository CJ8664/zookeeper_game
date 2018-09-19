#!/usr/bin/python

import logging
import re
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

        try:
            # Create client
            self.zk = KazooClient(hosts=ip_port, logger=logging)
            self.zk.start()
        except Exception as ex:
            print('Error connecting the Zookeeper Service, Please make sure the service is up or the IP:PORT provided is correct')
            sys.exit(-1)

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
    if arg_count != 3 or arg_count != 6:
        print('Invalid number of arguments provided, exiting...')
        sys.exit(-1)

    if arg_count == 6:
        # IP:PORT Name count mean_delay mean_score
        try:
            player_turns = int(sys.argv[3])
        except Exception as ex:
            print('Please provide a valid value of count')
            sys.exit(-1)

        try:
            u_delay = float(sys.argv[4])
        except Exception as ex:
            print('Please provide a valid value of u_delay')
            sys.exit(-1)

        try:
            u_score = float(sys.argv[5])
        except Exception as ex:
            print('Please provide a valid value of u_score')
            sys.exit(-1)

    try:
        # IP:PORT
        ip_port = sys.argv[1].split(':')
        if len(ip_port) == 1:
            ip_port = '{}:6000'.format(ip_port[0])
        else:
            ip_port = sys.argv[1]

        if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,4}$", ip_port):
            print('Please enter a valid IP address')
            sys.exit(-1)
    except Exception as ex:
        print('Please enter a valid IP address')
        sys.exit(-1)

    name = sys.argv[2]
    if name == '':
        print('Please enter a valid Player Name')
        sys.exit(-1)


    player = Player(ip_port, name)

    print('Starting Player at {} with name {}\n'.format(ip_port, name))
    if name in set(player.party):
        print('Player {} is already online, exiting...'.format(name))
        sys.exit(-1)
    player.join_party()

    try:
        if player_turns == -1: # Interactive mode
            while True:
                print('Enter Score: '),
                score = float(raw_input())
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
