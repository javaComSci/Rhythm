#!/bin/bash
# Takes in midi file as main parameter, requires file to exist in same directory

str=${1}
echo $str
find=".mid"
replace=".mp3"
result=${str//$find/$replace}
echo $result
rm $result
timidity /home/Rhythm/Backend/$str -Ow -o - | ffmpeg -i - -acodec libmp3lame -ab 64k $result
