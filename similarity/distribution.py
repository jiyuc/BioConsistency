import sent2vec
import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from tool.preprocess import normalise
from scipy.spatial import distance
import glob
from obj.goa import Brat

class Retriever:
    """
    This class implement distributional semantic sim measures
    """
    def __init__(self,model='sent2vec',pre_trained_model_path=''):
        self.s2v_model = None
        if model == 'sent2vec':
            try:
                self.s2v_model = sent2vec.Sent2vecModel()
                self.s2v_model.load_model(pre_trained_model_path)
            except Exception as e:
                print(e)
            print('pretrained model {} successfully loaded'.format(pre_trained_model_path))


    def cosine_sim(self, query, text):
        if not self.s2v_model:
            return 0
        if query == '' or text == '':
            return 0
        query = self.s2v_model.embed_sentence(normalise(query))
        text = self.s2v_model.embed_sentence(normalise(text))
        cosine_sim = 1 - round(distance.cosine(query, text),2)
        return cosine_sim

    def sent2vec_retrieval(self,query,document,min_score=0):
        if not query or query.evidence.text == '':
            return []
        if not document:
            return []
        if not self.s2v_model:
            return []

        sents = [s.evidence.text for s in document]

        scores = list()
        for i in range(len(sents)):
            try:
                gos = Brat().get_potential_go_ids(document[i].annotation_id)
            except FileNotFoundError: # no go term detected using conceptmapper, skip
                continue
            if query.goa.go_id not in gos:
                continue
            score = self.cosine_sim(query.evidence.text,sents[i])
            if score > min_score:
                scores.append((round(score,2),document[i]))
        if len(scores):
            return sorted(scores,reverse=True,key=lambda x:x[0])
        else: return []

