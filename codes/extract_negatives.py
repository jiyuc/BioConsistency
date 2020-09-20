import glob
import bioc
from textblob import TextBlob
from tqdm import tqdm
from instance import Instance
from command_parse import parse_command


class NegativeEx:

    def __init__(self):
        args = parse_command()
        self.bioc_annotation_xml_path = args.ann+'*.xml'
        self.bioc_document_xml_path = args.doc+'*.xml'
        self.output_txt_path = args.out

    def parse_bioc_text_span(self,passage_offset, annotation):
        """
        This method extract evidence sentence text spans.
        NOTE: The start of each text span calculates relative location to the start
        of its located paragraph (not the start of document)

        :param passage_offset: paragraph offset
        :param annotation: bioc annotation
        :return: list of text spans tuple (start, end)
        """
        if not annotation.locations:
            return []
        starts = list()
        ends = list()
        for location in annotation.locations:
            starts.append(location.offset - passage_offset) # relative location to the start of each paragraph(passage)
            ends.append(location.offset + location.length - passage_offset)
        return list(zip(starts, ends))


    def merge_overlapping_text_span(self,text_spans):
        """
        This method will merge overlapping text_spans into longer span
        e.g. (19,27) & (19, 29) will merge into (19,29)

        :param text_spans: a list pf text spans, sorted by start position
        :return: list of merged text spans
        """
        new_spans = list()
        last_start, last_end = 0, 0

        for start, end in text_spans:
            if start >= last_start and start <= last_end:
                last_end = max(end, last_end)
            elif start > last_end:
                if last_end > 0:
                    new_spans.append((last_start, last_end))
                last_start, last_end = start, end
        new_spans.append((last_start, last_end))
        return new_spans

    def resolve_positive_text_spans_index(self,annotation_path):
        """
        This method will extract BC4GO annotations.xml file;
        the annotations will be transformed into a dictionary structure

        :param: annotation_path: file directory of bc4go xml annotation files
        :return: hashmap structure: (key)docid, passage_id
                                    (value)list of merged evidence text_spans
        """
        positive_spans_index = dict()
        annotation_files = glob.glob(annotation_path)
        print("loading {} xml files from: {}" .format(str(len(annotation_files)),annotation_path))
        for filename in tqdm(annotation_files):
            with bioc.BioCXMLDocumentReader(filename) as collections:
                for doc in collections:  # in BC4GO, only one doc per collection
                    docid = doc.id
                    for passage in doc.passages:
                        doc_spans = list()
                        for annotation in passage.annotations:
                            try:
                                positive_spans = self.parse_bioc_text_span(passage.offset, annotation)
                            except: # the current annotation does not contain text span info
                                continue
                            doc_spans += positive_spans
                        positive_spans_index[(docid, passage.offset)] = self.merge_overlapping_text_span(
                                                         sorted(list(set(doc_spans)),key=lambda x: x[0]))
        print("Found {} TPs (merged)".format(str(len(positive_spans_index.values()))))
        return positive_spans_index

    def calculate_negative_text_spans_index(self,positive_text_spans_index):
        """
        This method calculate negative text spans by providing positive text spans
        e.g. positive (19,20), (25, 29) -> negative (21,24), (30,0)

        :param bc4go_annotations: dictionary of positive text spans. (key) docid,passageid
                                                                     (value) list((start,end))
        :return negative_text_spans: dictionary of negative text spans. (key) docid,passageid
                                                                        (value) list((start,end))
        """
        negative_text_spans_index = dict()
        for ann_id, positive_text_spans in positive_text_spans_index.items():
            last_start, last_end = 0, 0
            spans = list()
            for start, end in positive_text_spans:
                if last_end:
                    new_start = last_end + 1
                    new_end = start - 1
                    if new_start != new_end + 1:
                        spans.append((new_start, new_end))
                last_start, last_end = start, end
            spans.append((last_end + 1, 0))
            negative_text_spans_index[ann_id] = spans
            #print("positive:",positive_spans_index[ann_id])
            #print("negative",ann_id,spans)
        print("{} negative spans extracted".format(str(len(negative_text_spans_index.values()))))
        return negative_text_spans_index

    def sentence_segmentation(self,text):
        """
        This method segment a block of text into sentences.

        :param text: str typed texts
        :return: list of segmented sentences
        """
        blob = TextBlob(text)
        sentences = [str(s) for s in blob.sentences]
        if len(sentences):
            return sentences
        else:
            return [text]

    def resolve_section_info(self, passage, section_info):
        """
        This method will resolve the section info of a paragraph.
        If the passage is a front, level-1 title or abstract,
        the :section_info will be modified by passage_infons_type;
        Otherwise, the section_info will be retained will passed

        :param passage: bioc passages
        :param section_info: section_info of previous paragraph
        :return: resolved section info
        """
        if not section_info:
            return "#section_info" # no section_info is provided

        if 'front' in  passage.infons['type']:
            section_info = 'paper_title'
        elif 'title_1' in passage.infons['type']:
            section_info = passage.text
        elif 'abstract' in passage.infons['type']:
            section_info = 'abstract'
        return section_info

    def resolve_text_type(self,passage):
        if 'fig_caption' in passage.infons['type']: # text within fig caption
                return "#fig_caption"
        return "#main_body"

    def text_span_to_text(self,passage_text, text_spans):
        """
        This method will extract sub-texts from :passage_text
         given a list of :text_spans

        :param passage_text: raw string passage
        :param text_spans: a list of resolved text_spans
        :return: raw string passage with only text within the text_spans extracted
        """

        negative_text = ''
        if text_spans == None:  # all text in paragraph are negative
            negative_text = passage_text
        else:
            for (start, end) in text_spans:  # extract non-evidence texts
                if negative_text == '':
                    negative_text = passage_text[start:end]  # first sentence in a paragraph
                else:
                    negative_text += ' ' + passage_text[start:end]  # following sentences in a paragraph
        return negative_text

    def form_instance(self,docid,passage,section_info,text):
        instance = Instance()
        instance.evidence.text_type = self.resolve_text_type(passage)
        instance.evidence.docid = docid
        instance.evidence.passage_offset = passage.offset
        instance.evidence.text = text
        """if section_info == '#fig_caption':
            instance.text = text
        else:
            instance.text = ':'.join(self.sentence_segmentation(text))"""
        instance.evidence.section_info = section_info
        return instance

    def negative_instance_collection(self,text_spans):
        """
        This method will extract negative texts given negative texts spans
        of a full-length article. The extracted text will be sentence segmented
        using Textblob and stored into PMID.txt file. Each sentence has info:
        docid|paragraph_offset|section_info(e.g.Abstract)|text_location(e.g. main body)|text.

        :param text_spans: a dictionary of negative text_spans key: (docid,para_offset)| value: [(start,end)]
        :return:FileIO. *.txt files will be stored in :self.output_txt_path
        """
        files = glob.glob(self.bioc_document_xml_path)
        instances = list()
        for filename in files:
            with bioc.BioCXMLDocumentReader(filename) as collections:
                for doc in collections:
                    docid = doc.id
                    section_info = 'paper_title'
                    for passage in doc.passages:
                        section_info = self.resolve_section_info(passage, section_info)
                        if passage.infons['type'] == 'title_1':
                            continue # section info (e.g. abstract, introduction, results)

                        negative_text_spans = text_spans.get((docid, passage.offset))
                        negative_text = self.text_span_to_text(passage.text,negative_text_spans)

                        instance = self.form_instance(docid,passage,section_info,negative_text)
                        instances.append(instance)
        return instances

    def resolve_negative_instance_collection(self,instances):
        iid = 1
        docid = ''
        for instance in instances:
            if docid != instance.evidence.docid:
                iid = 1
            if instance.evidence.section_info == 'fig_caption':
                docid = instance.evidence.docid
                instance.annotation_id = '_'.join((docid,str(iid)))
                self.instance_totxt(self.output_txt_path, template_instance)
                iid += 1
            else:
                template_instance = instance
                sentences = self.sentence_segmentation(instance.evidence.text) # segment sentences
                sentences = self.formatting_figure_caption(sentences) # concatenate fig descriptions
                for s in sentences:
                    template_instance.evidence.text = s
                    docid = instance.evidence.docid
                    template_instance.annotation_id = '_'.join((docid,str(iid)))
                    self.instance_totxt(self.output_txt_path,template_instance)
                    iid += 1
        return True

    def instance_totxt(self,file_path,instance,appending=True):
        if appending:
            with open(file_path+instance.evidence.docid+'.txt','a',encoding='utf-8') as wf:
                wf.write(instance.tostring())
            wf.close()
        return True

    def formatting_figure_caption(self,sentences):
        """
        This method will reconcatenate fig descriptions that
        are segmented by textblob sentence segmentation
        e.g. reconcatenate "Fig." "1" -> "Fig. 1"

        :param sentences: a list of sentences
        :return: reformated sentences
        """
        template = ''
        new_sentences = list()
        for sent in sentences:
            if sent[-4:] == 'Fig.' or sent[-5:] == 'Figs.':
                template = sent
            elif template != '':
                template += ' '+sent
                new_sentences.append(template)
                template = ''
            else:
                new_sentences.append(sent)
        return new_sentences


if __name__ == '__main__':

    # create a instance generator
    negative_generator = NegativeEx()

    # extract TP sentences text spans in bc4go xml annotation files
    positive_spans_index = negative_generator.resolve_positive_text_spans_index(negative_generator.bioc_annotation_xml_path)

    # resolve negative spans
    negative_spans_index = negative_generator.calculate_negative_text_spans_index(positive_spans_index)

    #extract TN sentences
    instances = negative_generator.negative_instance_collection(negative_spans_index)

    # reformatting extracted TN sentences
    negative_generator.resolve_negative_instance_collection(instances)