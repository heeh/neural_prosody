import sys
import os
import typing
from sys import stdin, stdout
from collections import Counter
from collections import defaultdict
from prettytable import PrettyTable


path = os.getcwd() + "/input/tiny/"
stoptokens = ['HiF0', '*', '<', '>', '%r', '24.67']

tokens = []
nfinal_ip_tokens = Counter()
final_ip_tokens = Counter()

nf_ip_phrase = []
final_ip_phrase = []
ip_phrase = []

end_symbols = set(['H-H%','H-L%','L-H%','L-L%','!H-L%'])
ip_end_symbols = set(['H-','L-','!H-'])
collapse_cand = set(['!H*','L+!H*','L*+!H','!H-', '!H-L%'])

token_counts = Counter()
uni_counter = Counter()

uni_ip_counter = Counter()
uni_ending_counter = Counter()
uni_ip_lm = defaultdict(Counter)
uni_ending_lm = defaultdict(Counter)

ip_counter = defaultdict(Counter)
ending_counter = defaultdict(Counter)
uni_lm = defaultdict(Counter)
ip_lm = defaultdict(Counter)
ending_lm = defaultdict(Counter)

def analyze() -> None:
    for filename in os.listdir(path):
        inf = open(path + filename, "r")
        lines = inf.readlines()[8:]
        for i in range(len(lines)):
            target = lines[i].rstrip('\n').split()
            if(len(target) == 3):
                if('?' not in target[2] and target[2] not in stoptokens):
                    tokens.append(target[2])

    ph = ''
    big_ph = ''
    for token in tokens:
        # Collapse downstep symbols by Dinora's assumption
        if token in collapse_cand:
            token = token.replace('!','')
        ph += token + ' '
        big_ph += token + ' '
        if token in end_symbols:
            ip_phrase.append(big_ph)
            big_ph = ''
            final_ip_phrase.append(ph.rstrip())
            final_ip_tokens.update(ph.split())
            ph = ''
        elif token in ip_end_symbols:
            nf_ip_phrase.append(ph.rstrip())
            nfinal_ip_tokens.update(ph.split())
            ph = ''
        else:
            pass

    token_counts.update(tokens)    

    # ALL
    for k,v in token_counts.items():
        uni_counter[k] = v

    for k,v in token_counts.items():
        uni_lm[k] = v / len(tokens)

    for ph in nf_ip_phrase:
        phr_list = ph.split()
        for j in range(len(phr_list)):
            if(phr_list[j] not in['%H','H-','L-']):
                uni_ip_counter[phr_list[j]] += 1
        for j in range(len(phr_list)-1):
            ip_counter[phr_list[j]][phr_list[j+1]] += 1

    for curw, freq_dict in ip_counter.items():
        for nextw, freq in freq_dict.items():
            if nfinal_ip_tokens[curw] != 0:
                ip_lm[curw][nextw] = freq_dict[nextw] / nfinal_ip_tokens[curw]

    # ENDING(Uni, Bi)
    for ph in final_ip_phrase:
        phr_list = ph.split()
        for j in range(len(phr_list)):
            if(phr_list[j] not in['%H','H-','L-','H-H%','H-L%','L-H%','L-L%']):
                uni_ending_counter[phr_list[j]] += 1

        for j in range(len(phr_list)-1):
            ending_counter[phr_list[j]][phr_list[j+1]] += 1

    for curw, freq_dict in ending_counter.items():
        for nextw, freq in freq_dict.items():
            if final_ip_tokens[curw] != 0:
                ending_lm[curw][nextw] = freq_dict[nextw] / final_ip_tokens[curw]

    uni_sum = 0.0
    ending_sum = 0.0
    for k,v in uni_ip_counter.items():
        uni_sum += v
    for k,v in uni_ip_counter.items():
        uni_ip_lm[k] = v / uni_sum
    for k,v in uni_ending_counter.items():
        ending_sum += v
    for k,v in uni_ending_counter.items():
        uni_ending_lm[k] = v / ending_sum
                
def printNumbers():
    print('# of IP')
    print(len(ip_phrase))

    for x in ip_phrase:
        print(x)
    print('# of final iP')
    print(len(final_ip_phrase))
    for x in final_ip_phrase:
        print(x)
    print('# of non-final iP')
    print(len(nf_ip_phrase))
    for x in nf_ip_phrase:
        print(x)

    print('# of tones')
    print(len(tokens))
    
def printDist(distname, counter, lm):
    print('---------------------------')
    print(distname)
    print('---------------------------')
    print('%6s | %6s | %s | %s' % ('Prev','Cur','freq', 'Prob'))
    print('---------------------------')
    for prev,d in lm.items():
        for cur,v in sorted(d.items(),key=lambda t: -t[1]):
            print('%6s | %6s | %4d |%2.2f' % (prev, cur, counter[prev][cur], lm[prev][cur]*100))
        print('---------------------------')                

def printToneMatrix(distname, counter, lm):
    print(distname + ' IP phrase transition')
    t = PrettyTable()
    domain = set()
    image = set()
    
    for prev, d in counter.items():
        domain.add(prev)
        for cur, freq in d.items():
            image.add(cur)

    domain = list(domain)
    image = list(image)
        

    t.field_names = ['\\'] + image
    for prev in domain:
        cur_row = []
        cur_row.append(prev)
        for cur in image:
            cur_row.append(counter[prev][cur])
        t.add_row(cur_row)
    print(t)

def printProb(uni_ip_lm, uni_ending_lm, ip_lm, ending_lm):
    print("Uni IP LM\n-------------")
    for k,v in uni_ip_lm.items():
        print("%s, %.3f"%(k,v))
    print("\nUni END LM\n----------")
    for k,v in uni_ending_lm.items():
        print("%s, %.3f"%(k,v))
    print("\nBi IP LM\n------------")
    for k,d in ip_lm.items():
        for k2,v in d.items():
            print("%s -> %s %.3f"%(k,k2,v))
    print("\nBi END LM\n-----------")
    for k,d in ending_lm.items():
        for k2,v in d.items():
            print("%s -> %s %.3f"%(k,k2,v))

def printPitchAccentMatrix():
    pass

def main()->None:
    global uni_lm
    global ip_lm
    global ending_lm

    global path
    if len(sys.argv) != 1:
        path = os.getcwd() + sys.argv[1]
    analyze()
    printNumbers()
    printToneMatrix("Non-final", ip_counter, ip_lm)
    printToneMatrix("Final", ending_counter, ending_lm)
    printProb(uni_ip_lm, uni_ending_lm, ip_lm, ending_lm)
    
main()
