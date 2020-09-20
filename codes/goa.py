class Gene():
    """
    Define gene class
    """
    def __init__(self):
        self.gene_name = "#gene_name"
        self.gene_synonyms = ["#gene_synonym"]

    def tostring(self):
        """
        This method convert a Gene object to string

        :return: string
        """
        gene_synonyms = ':'.join(self.gene_synonyms)
        return '|'.join((self.gene_name,gene_synonyms))

    def fromstring(self,s):
        """
        This method convert a string to a Gene object

        :param s: a string
        :return: a Gene object
        """
        if not s:
            return None

        gene = Gene()
        template = s.split('|')
        gene.gene_name = template[0]
        gene.gene_synonyms = template[1].split(':')
        return gene

class GOA:
    """
    Define gene ontology annotation (GOA) class
    A GOA class contain gene ontology info & gene info
    """
    def __init__(self):
        self.go_id = "#go_id"
        self.go_term = "#go_term"
        self.go_definition = "#go_definition"
        self.evidence_code = "#evidence_code"
        self.evidence_type = "#evidence_type"
        self.gene = Gene() # gene info

    def tostring(self):
        """
        This method convert a GOA object to string

        :return: string
        """

        gene = self.gene.tostring()
        return '|'.join((self.go_id,
                        self.go_term,
                        self.go_definition,
                        self.evidence_code,
                        self.evidence_type,
                        gene))

    def fromstring(self,s):
        """
        This method convert a string to a GOA object

        :param s: a string
        :return: a GOA object
        """
        if not s:
            return None

        goa = GOA()
        template = s.split('|')
        goa.go_id = template[0]
        goa.go_term = template[1]
        goa.go_definition = template[2]
        goa.evidence_code = template[3]
        goa.evidence_type = template[4]
        gene = '|'.join(template[5:])
        goa.gene = Gene().fromstring(gene)
        return goa