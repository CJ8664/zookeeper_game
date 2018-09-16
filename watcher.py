#!/usr/bin/python

import logging
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
    score_board_size = 25

    def __init__(self, ip_port, score_board_size):
        '''Initialize everyting for the watcher'''
        logging.basicConfig()
        self.score_board_size = score_board_size

        # Create client
        self.zk = KazooClient(hosts=ip_port, logger=logging)
        self.zk.start()

        # Ensure Paths
        self.zk.ensure_path("/csjain_queue")
        self.zk.ensure_path("/csjain_players")

        # Create Data structures
        self.score_queue = Queue(self.zk, "/csjain_queue")
        self.party = Party(self.zk, '/csjain_players')

        # Create Watchers
        _ = ChildrenWatch(self.zk, "/csjain_queue", self.process_score)
        _ = ChildrenWatch(self.zk, "/csjain_players", self.process_client)


    def print_recent_board(self):
        '''Print the formatted Recent Score Board'''
        if self.curr_score:
            print('Most recent scores')
            print('------------------')
            for player, score in self.curr_score:
                if player in self.online_players:
                    print('{}\t\t{}\t**'.format(player, score))
                else:
                    print('{}\t\t{}'.format(player, score))
            print('\n')


    def print_leader_board(self):
        '''Print the formatted Leader Board'''
        if self.high_score:
            print('Highest scores')
            print('--------------')
            for player, score in self.high_score:
                if player in self.online_players:
                    print('{}\t\t{}\t**'.format(player, score))
                else:
                    print('{}\t\t{}'.format(player, score))
            print('\n')


    def process_score(self, children):
        '''Process any new score that is posted'''
        if len(self.score_queue) > 0:
            chil = self.score_queue.get()

            # Update high score
            self.high_score.append(chil.split(':'))
            self.high_score = sorted(self.high_score, key=lambda x: int(x[1]), reverse=True)
            self.high_score = self.high_score[:min(len(self.high_score), self.score_board_size)]

            # Update current score
            if not self.curr_score:
                self.curr_score = [chil.split(':')]
            elif len(self.curr_score) < self.score_board_size:
                self.curr_score = [chil.split(':')] + self.curr_score
            else:
                self.curr_score = [chil.split(':')] + self.curr_score[:-1]

            self.print_recent_board()
            self.print_leader_board()

        return True


    def process_client(self, children):
        self.online_players = set(self.party)
        self.print_recent_board()
        self.print_leader_board()


def main():

    ip_port, score_board_size = sys.argv[1].split(':'), int(sys.argv[2])

    if len(ip_port) == 1:
        ip_port = '{}:6000'.format(ip_port[0])
    else:
        ip_port = ip_port[0]

    score_watcher = ScoreWatcher(ip_port, score_board_size)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt as ex:
        pass

if __name__ == '__main__':
    main()
