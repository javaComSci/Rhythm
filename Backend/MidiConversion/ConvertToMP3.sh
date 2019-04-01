#!/bin/bash
# Takes in midi file as main parameter, requires file to exist in same directory

str=${1}
find=".mid"
replace=".mp3"
result=${str//$find/$replace}
echo $result
timidity /home/ubuntu/Rhythm/Backend/MidiConversion/$str -Ow -o - | ffmpeg -i - -acodec libmp3lame -ab 64k /home/ubuntu/Rhythm/Backend/MidiConversion/$result
