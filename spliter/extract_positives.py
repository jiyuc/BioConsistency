import bioc
import glob
from collections import defaultdict
import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from spliter.extract_negatives import NegativeEx
from obj.instance import Instance
from tqdm import tqdm
from tool.command_parse import parse_command

class PositiveEx:
    def __init__(self):
        args = parse_command()
        self.bioc_annotation_xml_path = args.ann+'*.xml'
        self.output_txt_path = args.out
        return

    def parse_bioc_annotation(self, instance, annotation):

        try:
            instance.annotation_id = annotation.id
            instance.goa.gene.gene_name = annotation.infons['gene']
            instance.goa.go_term, instance.goa.go_id = annotation.infons['go-term'].split('|')
            instance.goa.evidence_code = annotation.infons['goevidence']
            instance.goa.evidence_type = annotation.infons['type']
            instance.evidence.text = annotation.text
        except:
            print('skipped', annotation.id) # skip annotations that are not GO
            return None
        return instance

    def save_positive_to_txt(self,instance,file_path,appending):
        if not instance:
            return None
        instance.save_instance_to_txt(instance,file_path,appending)

    def docid_pasageoffset_to_section(self,):
        """
        This method will resolve section type given (docid,passage_offset)
        :return:
        """


    def resolve_text_type(self,passage):
        if 'fig_caption' in passage.infons['type']: # text within fig caption
                return "#fig_caption"
        return "#main_body"


    def bioc2instance(self,docid,passage_offset,annotation):
        """
        This method will convert a bioc annotation into string format

        :param docid: document id (PMID)
        :param passage_offset:  paragrph offset
        :param annotation:  bioc annotation

        :return: s converted string
        """
        if not annotation:
            return None

        parser = NegativeEx()
        instance = Instance()
        instance = self.parse_bioc_annotation(instance, annotation)
        if not instance:
            return None
        instance.evidence.docid = docid
        instance.evidence.passage_offset = passage_offset
        instance.evidence.text_spans.text_spans = parser.parse_bioc_text_span(passage_offset, annotation)
        #print(instance.instance_tostring())
        return instance

    def bioc2txt(self):
        """
        convert bioc GOA-evidence to string

        :return FileIO
        """
        files = glob.glob(self.bioc_annotation_xml_path)

        for filename in tqdm(files):
            visited = defaultdict(list)
            with bioc.BioCXMLDocumentReader(filename) as collections:
                for doc in collections:
                    docid = doc.id # extract document id (PMID)
                    for passage in doc.passages:
                        text_type = self.resolve_text_type(passage)
                        passage_offset = passage.offset # extract passage_offset
                        for annotation in passage.annotations:
                            instance = self.bioc2instance(docid,passage_offset,annotation)

                            if not instance: # not a GO annotation
                                continue
                            if instance.goa.go_id in visited[instance.evidence.text]:
                                continue # duplicate annotation
                            visited[instance.evidence.text] = visited.get(instance.evidence.text,[])+[instance.goa.go_id]
                            instance.evidence.text_type = text_type
                            file_path = self.output_txt_path+docid+'.txt'
                            self.save_positive_to_txt(instance,file_path,appending=True)
        return True

if __name__ == '__main__':
    positive_extractor = PositiveEx()
    positive_extractor.bioc2txt()