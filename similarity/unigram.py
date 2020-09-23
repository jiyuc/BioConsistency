import glob
from sklearn.feature_extraction.text import TfidfVectorizer
from obj.instance import Instance
from tool.preprocess import normalise


class Retriever:
    def __init__(self):
        return

    def fit_tf_idf(self,document):
        """
        This method will construct tf_idf_matrix for each sentence in a collection of documents
        Each vector in the matrix is a sentence
        Each matrix is a document
        A list of matrix is the collection of documents

        :param document: a list of raw-text sentences
        :return: fitted tfidf_vectorizer
        """
        if not document:
            return False
        if not isinstance(document,list):
            return False

        tfidf_vectorizer = TfidfVectorizer(use_idf=True)
        tfidf_vectorizer.fit(document)
        return tfidf_vectorizer


    def transform_tf_idf(self,tf_idf_vectorizer, document):
        """

        :param tf_idf_vectorizer:
        :param document:
        :return:
        """
        if not tf_idf_vectorizer or not document:
            return False
        if not isinstance(document,list):
            return False

        return tf_idf_vectorizer.transform(document)


    def tf_idf_retrieval(self, query, document, min_score=0):
        """
        This method is a tf-idf retriever.

        :param query: raw text query, a string
        :param document: a list of Instance() typed instance as document
        :param min_score: only return text of document instances greater than min_score

        :return: [(score, instance)] sorted by score in decline
        """
        if not query or query == '':
            return []
        if not document:
            return []
        sents = [normalise(s.evidence.text) for s in document]
        tf_idf_vectorizer = self.fit_tf_idf(sents)
        tf_idf_matrix = self.transform_tf_idf(tf_idf_vectorizer,sents)

        query = normalise(query)
        scores = list()
        for i in range(tf_idf_matrix.shape[0]):
            score = 0
            for w in query.split(' '):
                if w not in tf_idf_vectorizer.get_feature_names():
                    continue
                    # w is OOV (out of vocab)
                score += tf_idf_matrix[i,tf_idf_vectorizer.get_feature_names().index(w)]
            if score > min_score:
                scores.append((round(score,2),document[i]))
        return sorted(scores,reverse=True,key=lambda x:x[0])

    def scores_totxt(self,scores,path):
        """
        This method will save ranked items to file
        :param scores: [(score, instance)]
        :return: FileIO
        """
        with open(path,'w', encoding='utf-8') as wf:
            for score, instance in scores:
                wf.write('\t'.join(str(score),instance.tostring())+'\n')
        wf.close()
        return





if __name__ == '__main__':
    query = 'Here we show that Cryptocephal (CRC), the Drosophila homolog of ATF4, is an ecdysone receptor coactivator that is specific for isoform B2.'

    # load raw texts
    document_path = '/Users/jiyuc/Documents/GitHub/BioCGOES/train_corpus/Negatives/*.txt'
    document = list()
    retriever = Retriever()
    files = glob.glob(document_path)
    for filename in files:
        with open(filename, 'r') as rf:
            for s in rf:
                instance = Instance().fromstring(s)
                document.append(instance)
        rf.close()
        scores = retriever.tf_idf_retrieval(query, document,0.5)
        print([(score,instance.tostring()) for score,instance in  scores])
        break
