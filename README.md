# Distributed Realtime Scoreboard
This is created using Apache's Zookeeper and Kazoo library written in python

## STEP #1
Clone the repository

``csjain@vm17-81:~$ git clone https://github.ncsu.edu/csjain/zookeeper_game.git``

## STEP #2
Change the active directory to repository folder

``csjain@vm17-81:~$ cd zookeeper_game``

## STEP #3
Run the make command. This will download all the necessary libraries and dependencies required for the program to run. It will also setup the environment.

``csjain@vm17-81:~/zookeeper_game$ make``

## STEP #4

Run your test/evaluation.

Note "18.216.162.108:2181" is where I have setup a zookeer service, please replace that by your IP address.

``
csjain@vm17-81:~/zookeeper_game$ watcher 18.216.162.108:2181 25
``

``
csjain@vm17-81:~/zookeeper_game$ player 18.216.162.108:2181 "Captain America" 100 5000 2
``

``
csjain@vm17-81:~/zookeeper_game$ player 18.216.162.108:2181 Chirag
``


## EXTRA:

I have created a small script that helps to launch few player in batch mode, this is just for convenience and should not be used for grading :P

``csjain@vm17-81:~/zookeeper_game$ ./test_client.sh 18.216.162.108:2181``
