
# Table of Contents

1.  [Prosody Distribution](#orge4602f0)
    1.  [1. bigram.py:](#orgb974103)
        1.  [0) Extract Boston Radio Speech Corpus](#orgd922272)
        2.  [1) Place "bu\_radio" directory in current directory.](#org3a46e7f)
        3.  [2) $sh reset.sh](#org5a06a58)
        4.  [3) $sh retrieve\_files.sh](#org2254c2d)
        5.  [4) $python3 preprocessing.py](#orgcd507f9)
        6.  [5) $python3 bigram.py](#org7792829)
    2.  [2. LSTM.ipynb:](#org81b28ad)
    3.  [3. BERT.ipynb:](#org9edcf76)



<a id="orge4602f0"></a>

# Prosody Distribution

This git repository contains three modules.


<a id="orgb974103"></a>

## 1. bigram.py:

A naive probabilistic model that prints out the conditional probability of tone
symbol. In order to execute, following procedure.


<a id="orgd922272"></a>

### 0) Extract Boston Radio Speech Corpus


<a id="org3a46e7f"></a>

### 1) Place "bu\_radio" directory in current directory.


<a id="org5a06a58"></a>

### 2) $sh reset.sh


<a id="org2254c2d"></a>

### 3) $sh retrieve\_files.sh


<a id="orgcd507f9"></a>

### 4) $python3 preprocessing.py


<a id="org7792829"></a>

### 5) $python3 bigram.py


<a id="org81b28ad"></a>

## 2. LSTM.ipynb:

Prosody detection and generation using pytorch LSTM. 
This code is accessible via <https://colab.research.google.com/drive/1FkxnOhl6sUztp70GeJW14e2xL5FdbIII>
Nevertheless, this .ipynb file contains previous output.


<a id="org9edcf76"></a>

## 3. BERT.ipynb:

Prosody detection and generation using
BERT-NER(<https://github.com/huggingface/transformers/tree/master/examples#named-entity-recognition>)
Shareable Link: <https://colab.research.google.com/drive/1rb89J8tkFog5avhhOiIzQcClC13t7lV1>

Contact me at heehcs@gmail.com if you have any question or comment.

