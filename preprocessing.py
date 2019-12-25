pitch_accent = True
bound_IP = False
bound_iP = False

import os
import typing
from sys import stdin, stdout
from collections import Counter
from collections import defaultdict
from prettytable import PrettyTable
from random import shuffle
from math import floor

#wrd: 0 ton: 1 pos: 2
input_path = [os.getcwd() + "/input/wrd_all/", os.getcwd() + "/input/ton_all/", os.getcwd() + "/input/pos_all/"]
wrd_path = input_path[0]
ton_path = input_path[1]
pos_path = input_path[2]
outpath = os.getcwd() + "/output/"
data_path = [os.getcwd() + "/output/train/", os.getcwd() + "/output/test/", os.getcwd() + "/output/dev/"]


# input_path = [os.getcwd() + "/tiny_input/wrd/", os.getcwd() + "/tiny_input/ton/", os.getcwd() + "/tiny_input/pos/"]
# wrd_path = input_path[0]
# ton_path = input_path[1]
# pos_path = input_path[2]
# outpath = os.getcwd() + "/tiny_output/"
# data_path = [os.getcwd() + "/tiny_output/train/", os.getcwd() + "/tiny_output/test/", os.getcwd() + "/tiny_output/dev/"]

stoptones = ['HiF0', '*', '<', '>', '%r', '24.67']
words = []
tones = []
poss  = []
labels = set()
nfinal_ip_tones = Counter()
final_ip_tones = Counter()
fileDict = Counter()

nf_ip_phrase = []
final_ip_phrase = []
ip_phrase = []


all_end_symbols = set(['H-H%','H-L%','L-H%','L-L%','!H-L%', 'H-','L-','!H-'])

end_symbols = set(['H-H%','H-L%','L-H%','L-L%','!H-L%'])
ip_end_symbols = set(['H-','L-','!H-'])
collapse_cand = set(['!H*','L+!H*','L*+!H','!H-', '!H-L%'])




'''
Disk -> Memory Modules
'''

def separate_files_from_dir(datadir):
    file_list = os.listdir(os.path.abspath(datadir))
    shuffle(file_list)
    t_split = 0.6
    v_split = 0.8
    train_bound = floor(len(file_list) * t_split)
    test_bound = floor(len(file_list) * v_split)

    training = file_list[:train_bound]
    testing = file_list[train_bound:test_bound]
    validating = file_list[test_bound:]
    return training, testing, validating


def parse_pos(filename: str) -> None:
    inf = open(pos_path + filename, "r")
    lines = inf.readlines()
    for line in lines:
        if line not in ['\n','\r\n']:
            target = line.rstrip('\n').split()
            poss.append(target[1])
    
        
def parse_wrd(filename: str) -> None:
    global words
    inf = open(wrd_path + filename, "r")
    lines = inf.readlines()[7:]
    time_begin = 0.0
    for i in range(len(lines)):
        target = lines[i].rstrip('\n').split()
        if(len(target) == 3):
            time_end = float(target[0])
            word = target[2]
            words.append([time_begin,time_end,word,''])
            time_begin = time_end
    
def parse_ton(filename: str) -> None:
    global tones
    inf = open(ton_path + filename, "r")
    lines = inf.readlines()[8:]
    for i in range(len(lines)):
        target = lines[i].rstrip('\n').split()
        if(len(target) == 3):
            if('?' not in target[2] and target[2] not in stoptones):
                target[2] = target[2].replace('!', '')
#                print(target[2])
                # Eliminating Downstep
                # if ton in collapse_cand:
                tones.append([float(target[0]),target[2]])

    ph = ''
    big_ph = ''
    for time, ton in tones:
        ph += ton + ' '
        big_ph += ton + ' '
        if ton in end_symbols:
            # Intonational phrase that includes multiple non-final IPs and one final IP.
            ip_phrase.append(big_ph.rstrip())
            big_ph = ''

            final_ip_phrase.append(ph.rstrip())
            final_ip_tones.update(ph.split())
            ph = ''

        elif ton in ip_end_symbols:
            nf_ip_phrase.append(ph.rstrip())
            nfinal_ip_tones.update(ph.split())
            ph = ''

'''
In memory operations
'''            
def align():
    global words
    global tones
    for w in words:
        for ton in tones:
            wordBegin = w[0]
            wordEnd = w[1]
            wordStr = w[2]
            tonTime = ton[0]
            tonStr = ton[1]
            if wordBegin <= tonTime < wordEnd:
                w[3] += '' + tonStr
        if w[3] == '':
            w[3] = 'O'


'''
Memory -> Disk Modules
'''
            
def write_words_and_tags(output_path):
    global words
    global poss
    words_output = open(output_path + "words.txt", "a+")
    tags_output = open(output_path + "tones.txt", "a+")
    poss_output = open(output_path + "poss.txt", "a+")

#    for w in words:
    for i in range(len(words)):
        words_output.write(words[i][2] + '\n')
        tags_output.write(words[i][3] + '\n')
        poss_output.write(poss[i] + '\n')
            
def write_ips_and_tones(output_path):
    global words
    global tones
    global poss

    for x in ['train', 'test', 'dev']:
        if x in output_path:
            if x == 'dev':
                conll_output = open(output_path + "dev.txt", "a+")
            else:
                conll_output = open(output_path + x + ".txt", "a+")
            break
        
    ip_output = open(output_path + "ip_word.txt", "a+")
    tone_output = open(output_path + "ip_tone.txt", "a+")
    pos_phrase_output = open(output_path + "ip_pos.txt", "a+")


    ips = []
    tones = []
    poss_phrase = []
    ip = ''
    ton = ''
    pos = ''
    idx = 0

    for i in range(len(words)):
        # BERT Pitch Accent
        if pitch_accent and '*' in words[i][3]:
            conll_output.write(words[i][2] + ' ' + 'B-*' + '\n')
        else:
            conll_output.write(words[i][2] + ' ' + 'O' + '\n')
        # # BERT Bound IP
        # if bound_IP and '%' in words[i][3]:
        #     conll_output.write(words[i][2] + ' ' + '%' + '\n')
        # else:
        #     conll_output.write(words[i][2] + ' ' + 'O' + '\n')
        # # BERT Bound iP
        # if bound_IP and '-' in words[i][3]:
        #     conll_output.write(words[i][2] + ' ' + '-' + '\n')
        # else:
        #     conll_output.write(words[i][2] + ' ' + 'O' + '\n')
        # Normal BERT
        # conll_output.write(words[i][2] + ' ' + words[i][3] + '\n')
        
        ip += words[i][2] + ' '
        ton += words[i][3] + ' '
        pos += poss[i] + ' '
        for es in all_end_symbols:
            if es in words[i][3]:
                conll_output.write('\n')
                ip = ip.rstrip()
                ton = ton.rstrip()
                pos = pos.rstrip()
                ips.append(ip)
                tones.append(ton)
                poss_phrase.append(pos)
                
                ip = ''
                ton = ''
                pos = ''
                break
            
    for ip in ips:
        ip_output.write(ip + '\n')
    for ton in tones:
        tone_output.write(ton + '\n')
    for pos in poss_phrase:
        pos_phrase_output.write(pos + '\n')




        
def main()->None:
    #We are interested in files that has tones
    training_file_names, testing_file_names, validating_file_names = separate_files_from_dir(ton_path)
    print("input:")
    print(training_file_names)
    print(testing_file_names)
    print(validating_file_names)

    #    for filename in os.listdir(ton_path):
    for i, myset in enumerate([training_file_names, testing_file_names, validating_file_names]):
        for filename in myset:
            global words
            global tones
            words = []
            tones = []
            nameonly = filename.split('.')[0]
            # Ensure 3 files exist
            if not os.path.exists(wrd_path + nameonly + '.wrd'):
                continue
            if not os.path.exists(ton_path + nameonly + '.ton'):
                continue
            if not os.path.exists(pos_path + nameonly + '.pos'):
                continue

            parse_wrd(nameonly + '.wrd')
            parse_ton(nameonly + '.ton')
            parse_pos(nameonly + '.pos')
            align()
            write_words_and_tags(data_path[i])
            write_ips_and_tones(data_path[i])
        # for all files
    # for all sets
    print("output:")
    print(data_path)

main()
