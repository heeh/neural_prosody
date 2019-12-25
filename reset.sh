#!/bin/bash
rm -r ./input/
rm -r ./output/
rm -r ./tiny_output/

#!/bin/bash
if [ ! -d "./input" ]
then
    mkdir input
    mkdir input/ton_all
    mkdir input/wrd_all
    mkdir input/pos_all
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
fi
if [ ! -d "./output" ]
then
    mkdir output/
    mkdir output/train
    mkdir output/test
    mkdir output/dev

    mkdir tiny_output/
    mkdir tiny_output/train
    mkdir tiny_output/test
    mkdir tiny_output/dev
fi


