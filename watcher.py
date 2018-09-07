#!/usr/local/bin/python3

import logging
import time

from kazoo.recipe.watchers import ChildrenWatch
from kazoo.client import KazooClient
from kazoo.recipe.queue import Queue


class ScoreWatcher:

    curr_score = []
    high_score = []

    def __init__(self):
        logging.basicConfig()
        self.zk = KazooClient(hosts='127.0.0.1:2181')
        self.zk.start()
        print('Watch begin')
        self.my_queue = Queue(self.zk, "/queue")
        cw = ChildrenWatch(self.zk, "/queue", self.process_score)


    def print_recent_board(self):
        print('Most recent scores')
        print('------------------')
        for player, score in self.curr_score:
            print('{}\t\t{}'.format(player, score))
        print('\n')


    def print_leader_board(self):
        print('Highest scores')
        print('--------------')
        for player, score in self.high_score:
            print('{}\t\t{}'.format(player, score))
        print('\n')


    def process_score(self, children):
        chil = self.my_queue.get()
        if chil:
            # Add high score
            self.high_score.append(chil.split(':'))
            self.high_score = sorted(self.high_score, key=lambda x: int(x[1]), reverse=True)
            self.high_score = self.high_score[:min(len(self.high_score), 20)]

            # Add current score
            if not self.curr_score:
                self.curr_score = [chil.split(':')]
            elif len(self.curr_score) < 20:
                self.curr_score = [chil.split(':')] + self.curr_score
            else:
                self.curr_score = [chil.split(':')] + self.curr_score[:-1]
            self.print_recent_board()
            self.print_leader_board()


def main():
    sw = ScoreWatcher()
    while True:
        time.sleep(1)


if __name__ == '__main__':
    main()
