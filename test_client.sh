#!/usr/bin/env bash
echo "Starting Player Captain America"
player $1 "Captain America" 100 5000 2 &
echo "Starting Player Thor"
player $1 "Thor" 100 5000 3 &
echo "Starting Player Smaug"
player $1 "Smaug" 100 5000 4 &
echo "Starting Player Bob"
player $1 "Bob" 100 5000 5 &
echo "Starting Player Prof Freeh"
player "Prof Freeh" 100 5000 6 &
echo "Starting Player Chirag"
player $1 Chirag

# for i in `ps awx | grep -i python | awk -F" " '{print $1}'`
# do
# kill -9 $i
# done
