
# Table of Contents

1.  [Prosody Distribution](#org92cfffe)
    1.  [1. bigram.py:](#org6461c75)
        1.  [0) Extract Boston Radio Speech Corpus](#org58b79d9)
        2.  [1) Place "bu\\<sub>radio</sub>" directory in current directory.](#orgbe5a599)
        3.  [2) $sh reset.sh](#org80f330d)
        4.  [3) $sh retrieve\\<sub>files.sh</sub>](#orga3e7152)
        5.  [4) $python3 preprocessing.py](#org23a3800)
        6.  [5) $python3 bigram.py](#orgb21b3e8)
    2.  [2. LSTM.ipynb:](#org6119821)
    3.  [3. BERT.ipynb:](#org9561adc)


<a id="org92cfffe"></a>

# Prosody Distribution

This git repository contains three modules.


<a id="org6461c75"></a>

## 1. bigram.py:

A naive probabilistic model that prints out the conditional probability of tone
symbol. In order to execute, following procedure.


<a id="org58b79d9"></a>

### 0) Extract Boston Radio Speech Corpus


<a id="orgbe5a599"></a>

### 1) Place "bu\\<sub>radio</sub>" directory in current directory.


<a id="org80f330d"></a>

### 2) $sh reset.sh


<a id="orga3e7152"></a>

### 3) $sh retrieve\\<sub>files.sh</sub>


<a id="org23a3800"></a>

### 4) $python3 preprocessing.py


<a id="orgb21b3e8"></a>

### 5) $python3 bigram.py


<a id="org6119821"></a>

## 2. LSTM.ipynb:

Prosody detection and generation using pytorch LSTM. 
This code is accessible via <https://colab.research.google.com/drive/1FkxnOhl6sUztp70GeJW14e2xL5FdbIII>
Nevertheless, this .ipynb file contains previous output.


<a id="org9561adc"></a>

## 3. BERT.ipynb:

Prosody detection and generation using
BERT-NER(<https://github.com/huggingface/transformers/tree/master/examples#named-entity-recognition>)
Shareable Link: <https://colab.research.google.com/drive/1rb89J8tkFog5avhhOiIzQcClC13t7lV1>

Contact me at heehcs@gmail.com if you have any question or comment.

