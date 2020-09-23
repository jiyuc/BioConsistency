from similarity.distribution import Retriever
from obj.instance import Instance
import glob
from tqdm import tqdm



def pending_document(directory):
    document = list()
    with open(directory,'r') as f:
        for line in f:
            document.append(Instance().fromstring(line))
    f.close()
    return document


def get_negative_path(path):
    return path.replace("positives","negatives")


def retrieval_totxt(instance,scores):
    path = '/Users/jiyuc/Documents/GitHub/bio/corpus/sent2vec_pairs/{}.txt'.format(instance.evidence.docid)
    with open(path,'a') as fp:
        fp.write(instance.tostring())
        for score, neg in scores:
            template = '\t'.join((str(score),neg.tostring()))
            fp.write(template)
        fp.write("##EndOfRet##\n")
    fp.close()

def retrieve():
    positive_document_path = '/Users/jiyuc/Documents/GitHub/bio/corpus/positives/*.txt'
    #negative_document_path = '/Users/jiyuc/Documents/GitHub/bio/corpus/negatives/{}.txt'
    model_path = '/Users/jiyuc/Downloads/BioSentVec_PubMed_MIMICIII-bigram_d700.bin'
    retriever = Retriever(pre_trained_model_path=model_path)
    pos_files = glob.glob(positive_document_path)
    for pos_filename in tqdm(pos_files):
        neg_filename = get_negative_path(pos_filename)
        document = pending_document(neg_filename)
        with open(pos_filename, 'r') as fp:
            for line in fp:
                instance = Instance().fromstring(line)
                scores = retriever.sent2vec_retrieval(instance.evidence.text, document,0.6)
                retrieval_totxt(instance,scores)
    return

if __name__ == '__main__':
    retrieve()
