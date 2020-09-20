#!/bin/bash

# change directories below
export ANN='/Users/jiyuc/Documents/GitHub/BioConsistency/corpus/annotations/'
export DOC='/Users/jiyuc/Documents/GitHub/BioConsistency/corpus/articles/'
export POS_OUT='/Users/jiyuc/Documents/GitHub/BioConsistency/corpus/positives/'
export NEG_OUT='/Users/jiyuc/Documents/GitHub/BioConsistency/corpus/negatives/'

# DO NOT change lines below
# generate negative instances
python extract_negatives.py --ann $ANN --doc $DOC --out $NEG_OUT

# generate positive instances
python extract_positives.py --ann $ANN --doc $DOC --out $POS_OUT