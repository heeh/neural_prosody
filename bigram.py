import sys
import os
import typing
from sys import stdin, stdout
from collections import Counter
from collections import defaultdict
from prettytable import PrettyTable

entire_sequence = ""

nuclear_accent_dict = Counter()


path = os.getcwd() + "/input/all/"
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
    global entire_sequence
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
        entire_sequence += token
        # Collapse downstep symbols by Dinora's assumption
        if token in collapse_cand:
            token = token.replace('!','')
        ph += token + ' '
        big_ph += token + ' '
        
        #if token in end_symbols:
        if '%' in token:
            ip_phrase.append(big_ph.rstrip())
            big_ph = ''
            final_ip_phrase.append(ph.rstrip())
            final_ip_tokens.update(ph.split())

            ph = ''
        elif '-' in token:
        #elif token in ip_end_symbols:
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

    # for x in ip_phrase:
    #     print(x)
    print('# of final iP')
    print(len(final_ip_phrase))
    # for x in final_ip_phrase:
    #     print(x)
    print('# of non-final iP')
    print(len(nf_ip_phrase))
    # for x in nf_ip_phrase:
    #     print(x)

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


# Python program for KMP Algorithm 
def KMPSearch(pat, txt):
    global nuclear_accent_dict
    M = len(pat) 
    N = len(txt) 
  
    # create lps[] that will hold the longest prefix suffix  
    # values for pattern 
    lps = [0]*M 
    j = 0 # index for pat[] 
  
    # Preprocess the pattern (calculate lps[] array) 
    computeLPSArray(pat, M, lps) 
  
    i = 0 # index for txt[] 
    while i < N: 
        if pat[j] == txt[i]: 
            i += 1
            j += 1
  
        if j == M: 
            #print("Found pattern at index " + str(i-j))
            nuclear_accent_dict[pat] += 1
            j = lps[j-1] 
  
        # mismatch after j matches 
        elif i < N and pat[j] != txt[i]: 
            # Do not match lps[0..lps[j-1]] characters, 
            # they will match anyway 
            if j != 0: 
                j = lps[j-1] 
            else: 
                i += 1
  
def computeLPSArray(pat, M, lps): 
    len = 0 # length of the previous longest prefix suffix 
  
    lps[0] # lps[0] is always 0 
    i = 1
  
    # the loop calculates lps[i] for i = 1 to M-1 
    while i < M: 
        if pat[i]== pat[len]: 
            len += 1
            lps[i] = len
            i += 1
        else: 
            # This is tricky. Consider the example. 
            # AAACAAAA and i = 7. The idea is similar  
            # to search step. 
            if len != 0: 
                len = lps[len-1] 
  
                # Also, note that we do not increment i here 
            else: 
                lps[i] = 0
                i += 1
  

def numNuclearTunesAll():
    final_seq = ""
    for ph in final_ip_phrase:
        final_seq += ph.replace(' ','')

    final_seq.replace(' ', '')
    print(final_seq)

#    print(entire_sequence)
#    txt = entire_sequence
    txt = final_seq
    # all_patterns = ["H*L-", "H*H-",
    #             "L*H-", "L*L-",
    #             "L+H*H-", "L+H*L-",
    #             "L*+HL-",  "L*+HH-",
    #             "H+!H*H-", "H+!H*L-",]
    all_patterns = ['H*','L*','L+H*', 'L*+H', 'H+!H*']

    
    for pat in all_patterns:
        KMPSearch(pat, txt) 

    allSumArr = [0] * 5
    for i in range(0,5):
        allSumArr[i] = nuclear_accent_dict[all_patterns[i]]
    

    IP_patterns = ["H*L-L%", "H*L-H%", "H*H-H%","H*H-L%",
                "L*L-H%","L*H-L%", "L*H-H%", "L*L-L%",
                "L+H*L-H%", "L+H*L-L%","L+H*H-H%", "L+H*H-L%",
                "L*+HL-L%","L*+HH-L%","L*+HH-H%","L*+HL-H%",
                "H+!H*L-L%", "H+!H*L-H%", "H+!H*H-L%", "H+!H*H-H%",]

    for pat in IP_patterns:
        KMPSearch(pat, txt) 


    IPsumArr = [0] * 5
    for i in range(0,5):
        for j in range(4 * i, (4 * i) + 4):
            IPsumArr[i] += nuclear_accent_dict[IP_patterns[j]]
    # print("all")
    # print(allSumArr)
    print("Final")
    print(IPsumArr)

    interSumArr = [0] * 5
    for i in range(5):
        interSumArr[i] = allSumArr[i] - IPsumArr[i]
    
    print("Nonfinal")
    print(interSumArr)

    sumFinal = 0
    sumNF = 0
    for i in range(5):
        sumFinal += IPsumArr[i]
        sumNF += interSumArr[i]

    print("Final")
    for i in range(5):
        print(IPsumArr[i] / sumFinal * 100)
    print("NF")
    for i in range(5):
        print(interSumArr[i] / sumNF * 100)

    



                
def numNuclearTunes():
    #print(entire_sequence)
    txt = entire_sequence
    pat1 = "H*L-L%"
    patterns = ["H*L-L%", "H*L-H%", "L+H*L-H%", "L+H*L-L%", "L*L-H%",
                "H+!H*L-L%", "H*H-L%", "L+H*H-L%", "H+!H*L-H%", "L*L-L%",
                "H*H-H%", "L*+HL-L%", "L+H*H-H%", "L*H-L%", "L*H-H%",
                "L*+HH-L%", "L*+HL-H%", "H+!H*H-L%", "H+!H*H-H%", "L*+HH-H%"]
    for pat in patterns:
        KMPSearch(pat, txt) 

    sumOccur = 0
    for pat in patterns:
        sumOccur += nuclear_accent_dict[pat]
        print("%s + %d" % (pat, nuclear_accent_dict[pat]))

    for pat in patterns:
        print("%s + %.4f" % (pat, nuclear_accent_dict[pat]/sumOccur*100))

def numIntermediatePhrase():
    print("numIntermediatePhrase()")
    numIntermediatePhraseList = [0] * 10
    for ip in ip_phrase:
        cnt = 0
        for c in ip:
            if c == '-':
                cnt += 1
        numIntermediatePhraseList[cnt] += 1

    sumInter = 0
    for i in range(1,8):
        sumInter += numIntermediatePhraseList[i]
    for i in range(1,8):
        print(numIntermediatePhraseList[i])
    for i in range(1,8):
        print(numIntermediatePhraseList[i] / sumInter * 100)

        
def numPitchAccents():
    nf_numAccentList = [0] * 10
    f_numAccentList = [0] * 10
    
    # print(nf_ip_phrase[:5])
    # print(final_ip_phrase[:5])
    # print(ip_phrase[:5])

    for nfip in nf_ip_phrase:
        cnt = 0
        for c in nfip:
            if c == '*':
                cnt += 1
        nf_numAccentList[cnt] += 1
        # if cnt == 0:
        #     print(nfip)

    # print("nf_iP")
    # for i in range(10):
    #     print("#: %d freq: %d" % (i, nf_numAccentList[i]))


    for fip in final_ip_phrase:
        cnt = 0
        for c in fip:
            if c == '*':
                cnt += 1
        f_numAccentList[cnt] += 1

    # print("f_iP")
    # for i in range(10):
    #     print("#: %d freq: %d" % (i, f_numAccentList[i]))


    print("all_iP")
    for i in range(1,8):
        print("#: %d freq: %d" % (i, nf_numAccentList[i] + f_numAccentList[i]))

    
    sum_nf_num_accents = 0
    sum_f_num_accents = 0
    
    for i in range(1,8):
        sum_nf_num_accents += nf_numAccentList[i]
        sum_f_num_accents  +=  f_numAccentList[i]

    print("nf")
    for i in range(1,8):
        print(nf_numAccentList[i] / sum_nf_num_accents * 100)

    print("f")
    for i in range(1,8):
        print(f_numAccentList[i] / sum_f_num_accents * 100)

    print("all ip")
    for i in range(1,8):
        print((nf_numAccentList[i] + f_numAccentList[i]) / (sum_nf_num_accents + sum_f_num_accents) * 100)


                

def main()->None:
    global nuclear_accent_dict
    global entire_sequence
    global uni_lm
    global ip_lm
    global ending_lm
    global path
    if len(sys.argv) != 1:
        path = os.getcwd() + sys.argv[1]
    analyze()
    printNumbers()
    # printToneMatrix("Non-final", ip_counter, ip_lm)
    # printToneMatrix("Final", ending_counter, ending_lm)
    # printProb(uni_ip_lm, uni_ending_lm, ip_lm, ending_lm)
    # of Nuclear Tune Dist
    numNuclearTunesAll()
    #numNuclearTunes()
    # Number of accent in an intermediate phrase
    #numPitchAccents()
    #numIntermediatePhrase()
    
main()
