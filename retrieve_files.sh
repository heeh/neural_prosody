#!/bin/bash
find '/home/heeh/Downloads/bu_radio/data/f1a' -type f -name "*.ton" -exec cp {} ./ton_sample \;
find '/home/heeh/Downloads/bu_radio/data/f1a' -type f -name "*.wrd" -exec cp {} ./wrd_sample \;
