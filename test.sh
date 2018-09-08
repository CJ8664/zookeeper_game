#!/usr/bin/env bash
echo "Begin Testing on VCL"
echo "####################"
echo "Starting Watcher"
python watcher.py &
echo "####################"
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
