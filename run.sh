#!/bin/bash

# change directories below
# BC4GO corpus
export ANN='/Users/jiyuc/Documents/GitHub/bio/corpus/annotations/'
export DOC='/Users/jiyuc/Documents/GitHub/bio/corpus/articles/'

## directory for storing GO assiociated texts split from full-text articles
export POS_OUT='/Users/jiyuc/Documents/GitHub/bio/corpus/positives/'
## directory for storing non-GO assiociated texts split from full-text articles
export NEG_OUT='/Users/jiyuc/Documents/GitHub/bio/corpus/negatives/'
## directory for storing retrieved non-GO associated texts
export Retrieve_NEG_OUT='/Users/jiyuc/Documents/GitHub/bio/corpus/sent2vec_pairs/{}.txt'
## BioSent2Vec model (21GB). Downloaded from https://github.com/ncbi-nlp/BioSentVec
export S2VEC_MODEL='/Users/jiyuc/Downloads/BioSentVec_PubMed_MIMICIII-bigram_d700.bin'
## directory for storing "negation" direction swapped instances
export GO_SWAP='/Users/jiyuc/Documents/GitHub/bio/corpus/go_swapped_negatives/{}.txt'
## directory for storing GO specificity modified instances
export GO_SPE='/Users/jiyuc/Documents/GitHub/bio/corpus/go_replaced_negatives/{}.txt'
## directory for storing GO evidence code modified instances
export GO_ECODE='/Users/jiyuc/Documents/GitHub/bio/corpus/ec_replaced_negatives/{}.txt'

# DO NOT change lines below
# split texts without GO association
python spliter/extract_negatives.py --ann $ANN --doc $DOC --out $NEG_OUT

# split text with GO association
python spliter/extract_positives.py --ann $ANN --doc $DOC --out $POS_OUT

# tweak GOA info
python adversarial/tweak_goa.py --pos $POS_OUT --swap $GO_SWAP --specificity $GO_SPE --evicode $GO_ECODE

# retrieve TN text as negatives
python similarity/run_retrieval.py --pos $POS_OUT --model $S2VEC_MODEL --out $Retrieve_NEG_OUT