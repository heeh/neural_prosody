import os
import typing
from sys import stdin, stdout
from collections import Counter
from collections import defaultdict

#path = '/home/heeh/Dropbox/F19_LING696/Project/ton/'
path = os.getcwd() + "/ton/"


stoptokens = ['HiF0', '*', '<', '>', '%r', '24.67']
def main() -> None:
    tokens = []

    for filename in os.listdir(path):
        # print(filename)
        inf = open(path + filename, "r")
        lines = inf.readlines()[8:]
        for i in range(len(lines)):
            target = lines[i].rstrip('\n').split()
            if(len(target) == 3):
                if('?' not in target[2] and target[2] not in stoptokens):
                    tokens.append(target[2])

    # for i in range(len(tokens)):
    #     print(tokens[i])
    vocab = list(set(tokens))
    
    phrases = []
    ips = []
    end_symbols = set(['H-H%','H-L%','L-H%','L-L%'])
    ip_end_symbols = set(['H-','L-'])
    ph = ''
    for token in tokens:
        ph += ' ' + token
        if token in end_symbols:
            phrases.append(ph)
            ph = ''
        elif token in ip_end_symbols:
            ips.append(ph)
            ph = ''
        
    # for i, ph in enumerate(phrases):
    #     print(str(i) + ph)

    for s in phrases:
        s.split(' ')

    for s in ips:



    

    
    num_tokens = len(tokens)
    num_phrases = len(phrases)
    num_ips = len(ips)
    num_vocab = len(vocab)

    print('# of tokens : %d' % num_tokens)
    print('# of phrases: %d' % num_phrases)
    print('# of ips: %d' % num_phrases)
    print('# of types  : %d' % num_vocab)

    # for i, t in enumerate(vocab):
    #     print('%d %s '%(i,t))
        
    token_counts = Counter()
    token_counts.update(tokens)

    lm = defaultdict(Counter)
    ending_lm = defaultdict(Counter)
    ip_lm = defaultdict(Counter)



    word_counts = Counter()

    ending_counter = defaultdict(Counter)
    ip_counter = defaultdict(Counter)
    
    for k,v in token_counts.items():
        ending_counter[''][k] = v

    # Unigram
    for k,v in token_counts.items():
        lm[''][k] = v / num_tokens

    #Bigram(phrase)
    for ph in phrases:
        phr_list = ph.split()
        for j in range(len(phr_list)-1):
            ending_counter[phr_list[j]][phr_list[j+1]] += 1

    for curw, freq_dict in ending_counter.items():
        for nextw, freq in freq_dict.items():
            if token_counts[curw] != 0:
                ending_lm[curw][nextw] = freq_dict[nextw] / token_counts[curw]
    print('---------------------------')
    print('Ending Phrase')
    print('---------------------------')
    print('%6s | %6s | %s | %s' % ('Prev','Cur','freq', 'Prob'))
    print('---------------------------')
    for prev,d in ending_lm.items():
        for cur,v in sorted(d.items(),key=lambda t: -t[1]):
            print('%6s | %6s | %4d |%2.2f' % (prev, cur,ending_counter[prev][cur], ending_lm[prev][cur]*100))
        print('---------------------------')                



    #Bigram(ips)
    for ph in ips:
        phr_list = ph.split()
        for j in range(len(phr_list)-1):
            ip_counter[phr_list[j]][phr_list[j+1]] += 1

    for curw, freq_dict in ip_counter.items():
        for nextw, freq in freq_dict.items():
            if token_counts[curw] != 0:
                ip_lm[curw][nextw] = freq_dict[nextw] / token_counts[curw]
    print('---------------------------')
    print('IPs')
    print('---------------------------')
    print('%6s | %6s | %s | %s' % ('Prev','Cur','freq', 'Prob'))
    print('---------------------------')
    for prev,d in ip_lm.items():
        for cur,v in sorted(d.items(),key=lambda t: -t[1]):
            print('%6s | %6s | %4d |%2.2f' % (prev, cur,ip_counter[prev][cur], ip_lm[prev][cur]*100))
        print('---------------------------')                


    
main()
