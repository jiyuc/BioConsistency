#!/bin/bash

# change directories below
export ANN='/Users/jiyuc/Documents/GitHub/bio/corpus/annotations/'
export DOC='/Users/jiyuc/Documents/GitHub/bio/corpus/articles/'
export POS_OUT='/Users/jiyuc/Documents/GitHub/bio/corpus/positives/'
export NEG_OUT='/Users/jiyuc/Documents/GitHub/bio/corpus/negatives/'

# DO NOT change lines below
# generate negative instances
python spliter/extract_negatives.py --ann $ANN --doc $DOC --out $NEG_OUT

# generate positive instances
python spliter/extract_positives.py --ann $ANN --doc $DOC --out $POS_OUT