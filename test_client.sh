#!/usr/bin/env bash
echo "Starting Player Captain America"
python player.py "Captain America" &
echo "Starting Player Thor"
python player.py "Thor" &
echo "Starting Player Smaug"
python player.py "Smaug" &
echo "Starting Player Bob"
python player.py "Bob" &
echo "Starting Player Prof Freeh"
python player.py "Prof Freeh" &

# for i in `ps awx | grep -i python | awk -F" " '{print $1}'`
# do
# kill -9 $i
# done
