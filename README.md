# Distributed Realtime Scoreboard
This is created using Apache's Zookeeper and Kazoo library written in python

## STEP #1
Clone the repository

``git clone https://github.ncsu.edu/csjain/zookeeper_game.git``

## STEP #2
Change the active directory to repository folder

``cd zookeeper_game``

## STEP #3
Run the make command. This will download all the necessary libraries and dependencies required for the program to run. It will also setup the environment.

``make``

## STEP #4

Run your test/evaluation.

Note "18.216.162.108:2181" is where I have setup a zookeer service, please replace that by your IP address.

``
watcher 18.216.162.108:2181 25
``

``
player 18.216.162.108:2181 "Captain America" 100 5000 2
``

``
player 18.216.162.108:2181 Chirag
``
