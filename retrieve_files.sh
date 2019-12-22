#!/bin/bash
# for bigram
find './bu_radio/data/f1a' -type f -name "*.ton" -exec cp {} ./input/f1a \;
find './bu_radio/data/f2b' -type f -name "*.ton" -exec cp {} ./input/f2b \;
find './bu_radio/data/f3a' -type f -name "*.ton" -exec cp {} ./input/f3a \;
find './bu_radio/data/m1b' -type f -name "*.ton" -exec cp {} ./input/m1b \;
find './bu_radio/data/m2b' -type f -name "*.ton" -exec cp {} ./input/m2b \;
find './bu_radio/data/m3b' -type f -name "*.ton" -exec cp {} ./input/m3b \;
find './bu_radio/data/m4b' -type f -name "*.ton" -exec cp {} ./input/m4b \;

# for Neural net
find './bu_radio/data/f1a' -type f -name "*.ton" -exec cp {} ./input/ton_sample \;
find './bu_radio/data/f1a' -type f -name "*.wrd" -exec cp {} ./input/wrd_sample \;
find './bu_radio/data/f1a' -type f -name "*.pos" -exec cp {} ./input/pos_sample \;
find './bu_radio/data' -type f -name "*.ton" -exec cp {} ./input/ton_all \;
find './bu_radio/data' -type f -name "*.wrd" -exec cp {} ./input/wrd_all \;
find './bu_radio/data' -type f -name "*.pos" -exec cp {} ./input/pos_all \;

# for replication(Dainora)
find './bu_radio/data/f1a' -type f -name "*.ton" -exec cp {} ./input/dainora \;
find './bu_radio/data/f2b/labnews' -type f -name "*.ton" -exec cp {} ./input/dainora \;

# all
find './bu_radio/data/' -type f -name "*.ton" -exec cp {} ./input/all \;
