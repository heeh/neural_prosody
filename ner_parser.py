import os
import typing
from sys import stdin, stdout
from collections import Counter
from collections import defaultdict
from prettytable import PrettyTable

wrd_path = os.getcwd() + "/input/wrd_sample/"
ton_path = os.getcwd() + "/input/ton_sample/"
pos_path = os.getcwd() + "/input/pos_sample/"

outpath = os.getcwd() + "/output/"
train_path = os.getcwd() + "/output/train/"
test_path = os.getcwd() + "/output/test/"
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
                w[3] += '' + tonStr
        if w[3] == '':
            w[3] = 'O'
            


            
def write_words_and_tags(output_path):
    global words
    global poss
    words_output = open(output_path + "words.txt", "a")
    tags_output = open(output_path + "tobi_tones.txt", "a")
    poss_output = open(output_path + "poss.txt", "a")

#    for w in words:
    for i in range(len(words)):
        words_output.write(words[i][2] + '\n')
        tags_output.write(words[i][3] + '\n')
        poss_output.write(poss[i] + '\n')



            
def write_ips_and_tones(output_path):
    global words
    global tones
    global poss

    conll_output = open(output_path + "conll_output.txt", "a")
    ip_output = open(output_path + "intonational_phrase.txt", "a")
    tone_output = open(output_path + "tobi_tone_phrase.txt", "a")
    pos_phrase_output = open(output_path + "pos_phrase.txt", "a")


    ips = []
    tones = []
    poss_phrase = []
    ip = ''
    ton = ''
    pos = ''
    idx = 0
#    for w in words:
    for i in range(len(words)):
        conll_output.write(words[i][2] + ' ' + words[i][3] + '\n')
        
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
#        print(pos)
        pos_phrase_output.write(pos + '\n')


def push_labels():
    global labels
    for i in range(len(words)):
        labels.add(words[i][3])

def write_labels(label_path):
    global labels
    label_output = open(label_path + "labels.txt", "a")
    for lb in labels:
        if lb != 'O':
            label_output.write('B-' + lb + '\n')
        else:
            label_output.write(lb + '\n')

    

def main()->None:

    training_file_names, testing_file_names = separate_files_from_dir(ton_path)
    print(training_file_names)
    print(testing_file_names)

    if not os.path.exists('input'):
        os.makedirs('input')
        os.makedirs('input/sample_wrd')
        os.makedirs('input/sample_ton')
        os.makedirs('input/sample_pos')

    
    if not os.path.exists('output'):
        os.makedirs('output')
        os.makedirs('output/train')
        os.makedirs('output/test')


        
#    for filename in os.listdir(ton_path):
    for filename in training_file_names:
        init()
        nameonly = filename.split('.')[0]
        parse_wrd(nameonly + '.wrd')
        parse_ton(nameonly + '.ton')
        parse_pos(nameonly + '.pos')
        align()
        write_words_and_tags(train_path)
        write_ips_and_tones(train_path)
        push_labels()


        
    for filename in testing_file_names:
        init()
        nameonly = filename.split('.')[0]
        parse_wrd(nameonly + '.wrd')
        parse_ton(nameonly + '.ton')
        parse_pos(nameonly + '.pos')
        align()
        write_words_and_tags(test_path)
        write_ips_and_tones(test_path)
        push_labels()

    write_labels(outpath)

main()
