import os
import typing
from sys import stdin, stdout
from collections import Counter
from collections import defaultdict

#path = '/home/heeh/Dropbox/F19_LING696/Project/ton/'
path = os.getcwd() + "/ton/"


def main() -> None:
    tokens = []

    for filename in os.listdir(path):
        # print(filename)
        inf = open(path + filename, "r")
        lines = inf.readlines()[8:]
        for i in range(len(lines)):
            target = lines[i].rstrip('\n').split()
            if(len(target) == 3):
                tokens.append(target[2])

    # for i in range(len(tokens)):
    #     print(tokens[i])
    vocab = list(set(tokens))
    
    phrases = []
    end_symbols = set(['H-','L-','H-H%','H-L%','L-H%','L-L%'])
    ph = ''
    for token in tokens:
        ph += ' ' + token
        if token in end_symbols:
            phrases.append(ph)
            ph = ''
        
    # for i, ph in enumerate(phrases):
    #     print(str(i) + ph)


    
    num_tokens = len(tokens)
    num_phrases = len(phrases)
    num_vocab = len(vocab)

    print('# of tokens : %d' % num_tokens)
    print('# of phrases: %d' % num_phrases)
    print('# of types  : %d' % num_vocab)

    # for i, t in enumerate(vocab):
    #     print('%d %s '%(i,t))
        
    token_counts = Counter()
    lm = defaultdict(Counter)



    word_counts = Counter()
    token_counts.update(tokens)
    bigram_counter = defaultdict(Counter)
    
    for k,v in token_counts.items():
        bigram_counter[''][k] = v
    
    # Unigram
    for k,v in token_counts.items():
        lm[''][k] = v / num_tokens


    

    #Bigram
    for ph in phrases:
        phr_list = ph.split()
        for j in range(len(phr_list)-1):
            bigram_counter[phr_list[j]][phr_list[j+1]] += 1

    for curw, freq_dict in bigram_counter.items():
        for nextw, freq in freq_dict.items():
            if token_counts[curw] != 0:
                lm[curw][nextw] = freq_dict[nextw] / token_counts[curw]
    print('---------------------------')
    print('%6s | %6s | %s | %s' % ('Prev','Cur','freq', 'Prob'))
    print('---------------------------')
    for prev,d in lm.items():
        for cur,v in sorted(d.items(),key=lambda t: -t[1]):
            print('%6s | %6s | %4d |%2.2f' % (prev, cur,bigram_counter[prev][cur], lm[prev][cur]*100))
        print('---------------------------')                
        

    
main()
