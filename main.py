import os
import typing
from sys import stdin, stdout


#path = '/home/heeh/Dropbox/F19_LING696/Project/ton/'
path = os.getcwd() + "/ton/"


def main() -> None:
    tokens = []

    for filename in os.listdir(path):
        print(filename)
        inf = open(path + filename, "r")
        lines = inf.readlines()[8:]
        for i in range(len(lines)):
            target = lines[i].rstrip('\n').split()
            if(len(target) == 3):
                tokens.append(target[2])

    # for i in range(len(tokens)):
    #     print(tokens[i])

    phrases = []
    end_symbols = set(['H-','L-','H-H%','H-L%','L-H%','L-L%'])
    ph = ''
    for token in tokens:
        ph += ' ' + token
        if token in end_symbols:
            phrases.append(ph)
            ph = ''
        
    for i, ph in enumerate(phrases):
        print(str(i) + ph)

main()
