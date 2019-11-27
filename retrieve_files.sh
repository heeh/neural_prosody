#!/bin/bash
if [ ! -d "/path/to/dir" ]
then
    mkdir input
    mkdir input/ton_sample
    mkdir input/wrd_sample
    mkdir input/f1a
    mkdir input/f2b
    mkdir input/f3a
fi


find '/home/heeh/Downloads/bu_radio/data/f1a' -type f -name "*.ton" -exec cp {} ./input/ton_sample \;
find '/home/heeh/Downloads/bu_radio/data/f1a' -type f -name "*.wrd" -exec cp {} ./input/wrd_sample \;

find '/home/heeh/Downloads/bu_radio/data/f1a' -type f -name "*.ton" -exec cp {} ./input/f1a \;
#find '/home/heeh/Downloads/bu_radio/data/f1a' -type f -name "*.wrd" -exec cp {} ./f1a \;

find '/home/heeh/Downloads/bu_radio/data/f2b' -type f -name "*.ton" -exec cp {} ./input/f2b \;
#find '/home/heeh/Downloads/bu_radio/data/f2b' -type f -name "*.wrd" -exec cp {} ./f2b \;

find '/home/heeh/Downloads/bu_radio/data/f3a' -type f -name "*.ton" -exec cp {} ./input/f3a \;
#find '/home/heeh/Downloads/bu_radio/data/f3a' -type f -name "*.wrd" -exec cp {} ./f3a \;

