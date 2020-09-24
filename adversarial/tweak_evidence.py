from textblob import TextBlob
import glob
from obj.instance import Instance
from tqdm import tqdm


def insert_negation(instance):
    return


def reverse_info(instance):
    text = instance.evidence.text
    blob = TextBlob(text)
    adjectives = [w for w,tag in blob.tags if tag == 'JJ']
    adj_sieve = list()
    # filter-out irrelevant adjectives
    for w in adjectives:
        if 'activ' in w:
            adj_sieve.append(w)
        elif 'regula' in w:
            adj_sieve.append(w)
        elif 'creas' in w:
            adj_sieve.append(w)
        else:
            continue
    return adj_sieve



if __name__ == '__main__':
    positive_document_path = '/Users/jiyuc/Documents/GitHub/bio/corpus/positives/*.txt'
    #swapped_negative_path = '/Users/jiyuc/Documents/GitHub/bio/corpus/go_swapped_negatives/{}.txt'
    #go_replaced_negative_path = '/Users/jiyuc/Documents/GitHub/bio/corpus/go_replaced_negatives/{}.txt'
    instances = list()
    pos_files = glob.glob(positive_document_path)
    # load positives instances
    for pos_filename in tqdm(pos_files):
        with open(pos_filename, 'r') as fp:
            for line in fp:
                instances.append(Instance().fromstring(line))

    adjectives = list()
    for instance in instances:
        adjectives += reverse_info(instance)

    print(list(set(adjectives)))