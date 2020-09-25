import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from similarity.distribution import Retriever
from obj.instance import Instance
import glob
from tqdm import tqdm
from tool.command_parse import parse_retrieval_command



def pending_document(directory):
    document = list()
    with open(directory,'r') as f:
        for line in f:
            document.append(Instance().fromstring(line))
    f.close()
    return document


def get_negative_path(path):
    return path.replace("positives","negatives")


def retrieval_totxt(instance,scores,directory):
    path = directory.format(instance.evidence.docid)
    with open(path,'a') as fp:
        fp.write(instance.tostring())
        for score, neg in scores:
            template = '\t'.join((str(score),neg.tostring()))
            fp.write(template)
        fp.write("##EndOfRet##\n")
    fp.close()

def retrieve(positive_document_path,model_path,retrieved_document_path):

    retriever = Retriever(pre_trained_model_path=model_path)
    pos_files = glob.glob(positive_document_path)
    for pos_filename in tqdm(pos_files):
        neg_filename = get_negative_path(pos_filename)
        document = pending_document(neg_filename)
        with open(pos_filename, 'r') as fp:
            for line in fp:
                instance = Instance().fromstring(line)
                scores = retriever.sent2vec_retrieval(instance, document,0)
                if len(scores):
                    retrieval_totxt(instance,scores,retrieved_document_path)
                else:
                    continue
    return

if __name__ == '__main__':
    args = parse_retrieval_command()
    positive_document_path = args.pos+'*.txt'#'/Users/jiyuc/Documents/GitHub/bio/corpus/positives/*.txt'
    retrieved_document_path = args.out#'/Users/jiyuc/Documents/GitHub/bio/corpus/sent2vec_pairs/{}.txt'
    model_path = args.model#'/Users/jiyuc/Downloads/BioSentVec_PubMed_MIMICIII-bigram_d700.bin'
    retrieve(positive_document_path,model_path,retrieved_document_path)
