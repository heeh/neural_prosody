import os
import typing
from sys import stdin, stdout
from collections import Counter
from collections import defaultdict


from prettytable import PrettyTable


path = os.getcwd() + "/dainora/"
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
        # Collapse downstep symbols by Dinora
        if token in collapse_cand:
            token = token.replace('!','')
        ph += ' ' + token
        big_ph += ' ' + token
        if token in end_symbols:
            # Intonational phrase that includes multiple non-final IPs and one final IP.
            ip_phrase.append(big_ph)
            big_ph = ''

            final_ip_phrase.append(ph)
            final_ip_tokens.update(ph.split())
            ph = ''

        elif token in ip_end_symbols:
            nf_ip_phrase.append(ph)
            nfinal_ip_tokens.update(ph.split())
            ph = ''



    token_counts.update(tokens)    

    # ALL
    for k,v in token_counts.items():
        uni_counter[k] = v

    for k,v in token_counts.items():
        uni_lm[k] = v / len(tokens)

    # NF_IP_PHRASE(Uni, Bi)
    for ph in nf_ip_phrase:
        phr_list = ph.split()
        for j in range(len(phr_list)-1):
            ip_counter[phr_list[j]][phr_list[j+1]] += 1

    for curw, freq_dict in ip_counter.items():
        for nextw, freq in freq_dict.items():
            if nfinal_ip_tokens[curw] != 0:
                ip_lm[curw][nextw] = freq_dict[nextw] / nfinal_ip_tokens[curw]

    # ENDING(Uni, Bi)
    for ph in final_ip_phrase:
        phr_list = ph.split()
        for j in range(len(phr_list)-1):
            ending_counter[phr_list[j]][phr_list[j+1]] += 1

    for curw, freq_dict in ending_counter.items():
        for nextw, freq in freq_dict.items():
            if final_ip_tokens[curw] != 0:
                ending_lm[curw][nextw] = freq_dict[nextw] / final_ip_tokens[curw]


def printNumbers():
    print('# of ip phrases:')
    print(len(ip_phrase))

    print('# of non-final ip phrases:')
    print(len(nf_ip_phrase))
    print('# of final ip phrases:')
    print(len(final_ip_phrase))

    print('# of phrases:')
    print(len(nf_ip_phrase) + len(final_ip_phrase))
    print('# of tons')
    print(len(tokens))
    
    # print('nfinal_ip_tokens')
    # print(nfinal_ip_tokens)
    # print('final_ip_tokens')
    # print(final_ip_tokens)

                
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


def printPitchAccentMatrix():
    pass

    

def main()->None:
    analyze()
    printNumbers()
    # printDist('Non-final IP Distribution', ip_counter, ip_lm)
    # printDist('Final IP Distribution', ending_counter, ending_lm)
    printToneMatrix("Non-final", ip_counter, ip_lm)
    printToneMatrix("Final", ending_counter, ending_lm)
    #printPitchAccentMatrix()
    
main()
