# BioConsistency

Full description of the adversarial data generation is illustrated in paper:
### <Automatic Consistency Assurance for Literature-based Gene Ontology Annotation> (under peer review)


## Directories for data repositories
- The BC4GO corpus are stored within /corpus/annotation/*.xml and /corpus/annotation/*.txt
- Consistent instances are stored within /corpus/positives/*.txt
- Each *.txt file corresponds to an individual article in BC4GO named by it's PMID

## Term inconsistent instances
- (A) Contradictory inconsistencies are stored within /corpus/go_swapped_negatives/*.txt

- (B) Over-specific inconsistencies are stored within /corpus/go_replaced_negatives/*.txt

- (C) Unsupportive inconsistencies are stored within /corpus/sent2vec_pairs/*.txt. (The first line of each record is a consistent instance extracted from BC4GO. Following by lines of evidence text replaced instances as Unsupportive   inconsistencies. The first attribute are the cosine similarity score between BioSentVec of evidence text and BioSentVec of unsupportive text)

## Evidence code inconsistent instances
- (D) Error-code inconsistencies are stored within /corpus/ec_replaced_netatives/*.txt

## Re-generation of adversarial instances
- Change the directory for data depository in run.sh file
- Find select_go_child() function in /adversarial/tweak_goa.py and comment lines as instructed to able/disable application of training set optimisation
- run run.sh to re-generate instances if needed
