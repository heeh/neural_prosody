#!/bin/bash
if [ ! -d "./input" ]
then
    mkdir input
    mkdir input/ton_sample
    mkdir input/wrd_sample
    mkdir input/pos_sample
    mkdir input/all
    mkdir input/dainora
    
    mkdir input/f1a
    mkdir input/f2b
    mkdir input/f3a
    mkdir input/m1b
    mkdir input/m2b
    mkdir input/m3b
    mkdir input/m4b
    mkdir output/
    mkdir output/train
    mkdir output/test
    
fi
# for Neural net
find './bu_radio/data/f1a' -type f -name "*.ton" -exec cp {} ./input/ton_sample \;
find './bu_radio/data/f1a' -type f -name "*.wrd" -exec cp {} ./input/wrd_sample \;
find './bu_radio/data/f1a' -type f -name "*.pos" -exec cp {} ./input/pos_sample \;

# for bigram
find './bu_radio/data/f1a' -type f -name "*.ton" -exec cp {} ./input/f1a \;
find './bu_radio/data/f2b' -type f -name "*.ton" -exec cp {} ./input/f2b \;
find './bu_radio/data/f3a' -type f -name "*.ton" -exec cp {} ./input/f3a \;
find './bu_radio/data/m1b' -type f -name "*.ton" -exec cp {} ./input/m1b \;
find './bu_radio/data/m2b' -type f -name "*.ton" -exec cp {} ./input/m2b \;
find './bu_radio/data/m3b' -type f -name "*.ton" -exec cp {} ./input/m3b \;
find './bu_radio/data/m4b' -type f -name "*.ton" -exec cp {} ./input/m4b \;

# for replication(Dainora)
find './bu_radio/data/f1a' -type f -name "*.ton" -exec cp {} ./input/dainora \;
find './bu_radio/data/f2b/labnews' -type f -name "*.ton" -exec cp {} ./input/dainora \;


find './bu_radio/data/' -type f -name "*.ton" -exec cp {} ./input/all \;
