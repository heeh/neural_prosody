import os
import typing
from sys import stdin, stdout
from collections import Counter
from collections import defaultdict
from prettytable import PrettyTable

wrd_path = os.getcwd() + "/input/wrd_sample/"
ton_path = os.getcwd() + "/input/ton_sample/"
train_path = os.getcwd() + "/output/train/"
test_path = os.getcwd() + "/output/test/"
stoptones = ['HiF0', '*', '<', '>', '%r', '24.67']

words = []
tones = []

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




import os
from random import shuffle
from math import floor

def separate_files_from_dir(datadir):
    file_list = os.listdir(os.path.abspath(datadir))
    shuffle(file_list)
    split = 0.7
    split_index = floor(len(file_list) * split)
    training = file_list[:split_index]
    testing = file_list[split_index:]
    return training, testing


def init():
    global words
    global tones
    words = []
    tones = []


    
        
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
                tones.append([float(target[0]),target[2]])

    ph = ''
    big_ph = ''
    for time, ton in tones:
        # Collapse downstep symbols by Dinora
        if ton in collapse_cand:
            ton = ton.replace('!','')
        ph += ' ' + ton
        big_ph += ' ' + ton
        if ton in end_symbols:
            # Intonational phrase that includes multiple non-final IPs and one final IP.
            ip_phrase.append(big_ph)
            big_ph = ''

            final_ip_phrase.append(ph)
            final_ip_tones.update(ph.split())
            ph = ''

        elif ton in ip_end_symbols:
            nf_ip_phrase.append(ph)
            nfinal_ip_tones.update(ph.split())
            ph = ''

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
                w[3] += tonStr
        if w[3] == '':
            w[3] = '0'
            

def write_words_and_tags(output_path):
    global words
    words_output = open(output_path + "words.txt", "a")
    tags_output = open(output_path + "tags.txt", "a")

    for w in words:
        words_output.write(w[2] + '\n')
        tags_output.write(w[3] + '\n')


            
def write_ips_and_tones(output_path):
    global words
    global tones
    ip_output = open(output_path + "ips.txt", "a")
    tone_output = open(output_path + "tones.txt", "a")


    ips = []
    tones = []
    ip = ''
    ton = ''
    for w in words:
        ip += w[2] + ' '
        ton += w[3] + ' '
        for es in all_end_symbols:
            if es in w[3]:
                ip = ip.rstrip()
                ton = ton.rstrip()
                ips.append(ip)
                tones.append(ton)
                ip = ''
                ton = ''
                break
            
    for ip in ips:
        ip_output.write(ip + '\n')
    for ton in tones:
        tone_output.write(ton + '\n')


def main()->None:

    training, testing = separate_files_from_dir(ton_path)
    print(training)
    print(testing)

    if not os.path.exists('input'):
        os.makedirs('input')
        os.makedirs('input/sample_wrd')
        os.makedirs('input/sample_ton')

    
    if not os.path.exists('output'):
        os.makedirs('output')
        os.makedirs('output/train')
        os.makedirs('output/test')

    
#    for filename in os.listdir(ton_path):
    for filename in training:
        init()
        nameonly = filename.split('.')[0]
        parse_wrd(nameonly + '.wrd')
        parse_ton(nameonly + '.ton')
        align()
        write_words_and_tags(train_path)
        write_ips_and_tones(train_path)
        
    for filename in testing:
        init()
        nameonly = filename.split('.')[0]
        parse_wrd(nameonly + '.wrd')
        parse_ton(nameonly + '.ton')
        align()
        write_words_and_tags(test_path)
        write_ips_and_tones(test_path)


main()
