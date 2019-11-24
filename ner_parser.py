import os
import typing
from sys import stdin, stdout
from collections import Counter
from collections import defaultdict
from prettytable import PrettyTable

wrd_path = os.getcwd() + "/wrd_sample/"
ton_path = os.getcwd() + "/ton_sample/"

stoptones = ['HiF0', '*', '<', '>', '%r', '24.67']

words = []
tones = []

nfinal_ip_tones = Counter()
final_ip_tones = Counter()

nf_ip_phrase = []
final_ip_phrase = []
ip_phrase = []

end_symbols = set(['H-H%','H-L%','L-H%','L-L%','!H-L%'])
ip_end_symbols = set(['H-','L-','!H-'])
collapse_cand = set(['!H*','L+!H*','L*+!H','!H-', '!H-L%'])


class labeled_word:
    def __init__(self, begin:float, end:float, word:str, label:str):
        self.begin = begin
        self.end = end
        self.word = word
        self.label = label
    
def parse_wrd() -> None:
    print('parse_wrd()')
    for filename in os.listdir(wrd_path):
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
    


    
def parse_ton() -> None:
    print('parse_ton()')
    for filename in os.listdir(ton_path):
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
    for w in words:
        for ton in tones:
            wordBegin = w[0]
            wordEnd = w[1]
            wordStr = w[2]
            tonTime = ton[0]
            tonStr = ton[1]
            if wordBegin <= tonTime < wordEnd:
                w[3] += tonStr + ' '
            
            
            
            

def main()->None:
    parse_wrd()
    parse_ton()
    align()
    for w in words:
        print(w)

    

main()
