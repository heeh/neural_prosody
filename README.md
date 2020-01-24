
# Table of Contents

1.  [Prosody Distribution](#org09503da)
    1.  [1. bigram.py:](#org3e4dd2d)
        1.  [0) Extract Boston Radio Speech Corpus](#org0552386)
        2.  [1) Place "bu<sub>radio</sub>" directory in current directory.](#org6e51263)
        3.  [2) $sh reset.sh](#org0a77f7f)
        4.  [3) $sh retrieve<sub>files.sh</sub>](#org88627fb)
        5.  [4) $python3 preprocessing.py](#org652a53a)
        6.  [5) $python3 bigram.py](#org89e32d8)
    2.  [2. LSTM.ipynb:](#org3017c8c)
    3.  [3. BERT.ipynb:](#org63286e9)


<a id="org09503da"></a>

# Prosody Distribution

This git repository contains three modules.


<a id="org3e4dd2d"></a>

## 1. bigram.py:

A naive probabilistic model that prints out the conditional probability of tone
symbol. In order to execute, following procedure.


<a id="org0552386"></a>

### 0) Extract Boston Radio Speech Corpus


<a id="org6e51263"></a>

### 1) Place "bu<sub>radio</sub>" directory in current directory.


<a id="org0a77f7f"></a>

### 2) $sh reset.sh


<a id="org88627fb"></a>

### 3) $sh retrieve<sub>files.sh</sub>


<a id="org652a53a"></a>

### 4) $python3 preprocessing.py


<a id="org89e32d8"></a>

### 5) $python3 bigram.py


<a id="org3017c8c"></a>

## 2. LSTM.ipynb:

Prosody detection and generation using pytorch LSTM. 
This code is accessible via <https://colab.research.google.com/drive/1FkxnOhl6sUztp70GeJW14e2xL5FdbIII>
Nevertheless, this .ipynb file contains previous output.


<a id="org63286e9"></a>

## 3. BERT.ipynb:

Prosody detection and generation using
BERT-NER(<https://github.com/huggingface/transformers/tree/master/examples#named-entity-recognition>)
Shareable Link: <https://colab.research.google.com/drive/1rb89J8tkFog5avhhOiIzQcClC13t7lV1>

Contact me at heehcs@gmail.com if you have any question or comment.

