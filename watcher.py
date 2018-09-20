#!/usr/bin/python

import logging
import re
import sys
import time

from kazoo.client import KazooClient
from kazoo.recipe.party import Party
from kazoo.recipe.queue import Queue
from kazoo.recipe.watchers import ChildrenWatch


class ScoreWatcher:

    curr_score = []
    high_score = []
    online_players = set()

    def __init__(self, ip_port, score_board_size):
        '''Initialize everyting for the watcher'''
        logging.basicConfig()
        self.score_board_size = score_board_size
        self.is_dump = False
        self.is_init_score = True
        self.is_init_client = True

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
        self.score_queue = Queue(self.zk, '/csjain_queue')
        self.party = Party(self.zk, '/csjain_players')
        self.online_players = set(self.party)

        # Create Watchers
        _ = ChildrenWatch(self.zk, '/csjain_queue', self.process_score)
        _ = ChildrenWatch(self.zk, '/csjain_players', self.process_client)

    def print_scoreboards(self):
        '''Print the formatted Recent Score and Leader Board'''
        if self.is_dump:
            return

        print('Most recent scores')
        print('------------------')
        if self.curr_score:
            for player, score in self.curr_score:
                if player in self.online_players:
                    print('{}\t\t{}\t**'.format(player, score))
                else:
                    print('{}\t\t{}'.format(player, score))
            print('\n')

        print('Highest scores')
        print('--------------')
        if self.high_score:
            for player, score in self.high_score:
                if player in self.online_players:
                    print('{}\t\t{}\t**'.format(player, score))
                else:
                    print('{}\t\t{}'.format(player, score))
            print('\n')


    def process_score(self, children):
        '''Process any pending score or new score that is posted'''
        if not children:
            return True

        while len(self.score_queue) > 0 and not self.is_dump:
            new_score = self.score_queue.get()

            if not new_score:
                break

            # Update high score
            self.high_score.append(new_score.split(':'))
            self.high_score = sorted(self.high_score, key=lambda x: float(x[1]), reverse=True)
            self.high_score = self.high_score[:min(len(self.high_score), self.score_board_size)]

            # Update current score
            if not self.curr_score:
                self.curr_score = [new_score.split(':')]
            elif len(self.curr_score) < self.score_board_size:
                self.curr_score = [new_score.split(':')] + self.curr_score
            else:
                self.curr_score = [new_score.split(':')] + self.curr_score[:-1]

        self.print_scoreboards()
        return True


    def process_client(self, children):
        '''Process updates to a player joining or leaving the game'''
        if self.is_init_client:
            self.is_init_client = False
            return True

        self.online_players = set(self.party)
        if self.curr_score:
            self.print_scoreboards()

        return True

    def dump_scoreboard(self):
        self.is_dump = True
        for name, score in self.high_score:
            self.score_queue.put('{}:{}'.format(name, score).encode('utf-8'))


def main():

    arg_count = len(sys.argv)
    if arg_count != 3:
        print('Invalid number of arguments provided, exiting...')
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


    try:
        # Score Board Size
        score_board_size = int(sys.argv[2])
        if score_board_size > 25:
            print('Score Board size cannot be greater than 25, exiting...')
            sys.exit(-1)
    except Exception as ex:
        print('Please enter a valid Score Board size')
        sys.exit(-1)

    print('Starting Watcher at {} with score board size {}\n'.format(ip_port, score_board_size))
    score_watcher = ScoreWatcher(ip_port, score_board_size)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt as ex:
        score_watcher.dump_scoreboard()

if __name__ == '__main__':
    main()
