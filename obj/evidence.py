
class Evidence:
    """
    Define evidence class

    The evidence info include document id (PMID)
    passage_offset (relative offset to the start of the article)
    text_spans:
    section info: rhetorical zone where the evidence located (Introduction, Abstract, etc,.)
    text: raw text
    text_type: main body or figure captions or the article
    """

    def __init__(self):
        self.docid = "#docid"
        self.passage_offset = 0
        self.text_spans = Text_Spans() # text spans
        self.section_info = "#section_info"  # e.g. Introduction
        self.text = "#text"  # raw text
        self.text_type = "#text_type"  # mainbody or fig_caption

    def tostring(self):
        """
        This method converts an evidence object to a string

        :return: a string
        """
        text_spans = self.text_spans.tostring()
        s = '|'.join((self.docid,
                      str(self.passage_offset),
                      self.section_info,
                      text_spans,
                      self.text,
                      self.text_type))
        return s

    def fromstring(self,s):
        if not s:
            return None

        evidence = Evidence()
        template = s.split('|')
        evidence.docid = template[0]
        evidence.passage_offset = int(template[1])
        evidence.section_info = template[2]
        evidence.text_spans = Text_Spans().fromstring(template[3])
        evidence.text = template[4]
        evidence.text_type = template[5]
        return evidence



class Text_Spans:
    """
    Define text_span class
    text_spans are part of the evidence info;
    are a list of tuples in (start, end) structure
    """
    def __init__(self):
        self.text_spans = [(0,0)]

    def tostring(self):
        """
        This method converts a list of text_spans as tuples into single string
        :param text_spans: list((start1,end1),(start2,end2))
        :return:  str(start1:end1$$start2:end2)
        """
        if len(self.text_spans) == 0:
            return ""
        return '$$'.join(':'.join((str(start), str(end))) for (start, end) in self.text_spans)

    def fromstring(self,s):
        ts = Text_Spans()
        if not s or s == "":
            return None
        tuples = [t for t in s.split('$$')]
        spans = [(int(span.split(":")[0]),int(span.split(":")[1])) for span in tuples]
        ts.text_spans = spans
        return ts