"""
Approaches in this file extract only the evidence raw text from instance typed object.
"""
import glob
from obj.instance import Instance


def load_instances(directory):

    files = glob.glob(directory)
    instances = list()
    for filename in files:
        with open(filename,'r') as f:
            for line in f:
                instances.append(Instance().fromstring(line))
    return instances

def extract_raw_text(instances,directory):
    visited = set()
    for instance in instances:
        docid = instance.evidence.docid
        annid = str(instance.annotation_id)
        raw_text = instance.evidence.text+'\n'
        if raw_text in visited:
            continue
        visited.add(raw_text)
        f = open(directory.format(annid), 'a')
        f.write(raw_text)
    return 0



if __name__ == '__main__':
    directory = '/Users/jiyuc/Documents/GitHub/bio/corpus/negatives/*.txt'
    raw_directory = '/Users/jiyuc/Documents/GitHub/bio/corpus/negatives/raw/{}.txt'
    extract_raw_text(load_instances(directory),raw_directory)
