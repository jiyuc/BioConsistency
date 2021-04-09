#!/bin/bash

# change directories below as needed
# BC4GO corpus (provided)
export ANN='/corpus/annotations/'
export DOC='/corpus/articles/'

## directory for storing GO assiociated texts split from full-text articles
export POS_OUT='/corpus/positives/'
## directory for storing non-GO assiociated texts split from full-text articles
export NEG_OUT='/corpus/negatives/'
## BioSent2Vec model (21GB). Downloaded from https://github.com/ncbi-nlp/BioSentVec
# This is not provided in our repository
export S2VEC_MODEL='/BioSentVec_PubMed_MIMICIII-bigram_d700.bin'
## directory for storing Unsupportive instances
export Retrieve_NEG_OUT='/corpus/sent2vec_pairs/{}.txt'
## directory for storing "negation" direction swapped instances
export GO_SWAP='/corpus/go_swapped_negatives/{}.txt'
## directory for storing GO specificity modified instances
export GO_SPE='/corpus/go_replaced_negatives/{}.txt'
## directory for storing GO evidence code modified instances
export GO_ECODE='/corpus/ec_replaced_negatives/{}.txt'

# comment/discomment lines below as needed

## template, for extract texts that do not associate with any GO term and will be used to generate Unsupportive instances afterwards
python spliter/extract_negatives.py --ann $ANN --doc $DOC --out $NEG_OUT

## generate consistent instances (run run.sh to generate)
python spliter/extract_positives.py --ann $ANN --doc $DOC --out $POS_OUT

## generate Contradictory, Over-specific, Error-code inconsistencies (already provided)
#python adversarial/tweak_goa.py --pos $POS_OUT --swap $GO_SWAP --specificity $GO_SPE --evicode $GO_ECODE

## generate Unsupportive inconsistencies (already provided)
#python similarity/run_retrieval.py --pos $POS_OUT --model $S2VEC_MODEL --out $Retrieve_NEG_OUT
