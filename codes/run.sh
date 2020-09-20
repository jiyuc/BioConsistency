#!/bin/bash

# change directories below
export ANN='/Users/jiyuc/Documents/GitHub/BioConsistency/corpus/Annotations/'
export DOC='/Users/jiyuc/Documents/GitHub/BioConsistency/corpus/Articles/'
export POS_OUT='/Users/jiyuc/Documents/GitHub/BioConsistency/corpus/Positives/'
export NEG_OUT='/Users/jiyuc/Documents/GitHub/BioConsistency/corpus/Negatives/'

# DO NOT change lines below
# generate negative instances
python extract_negatives.py --ann $ANN --doc $DOC --out $NEG_OUT

# generate positive instances
python extract_positives.py --ann $ANN --doc $DOC --out $POS_OUT