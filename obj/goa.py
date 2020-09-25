import json
import requests, sys
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

    def query_go(self,query,flag='swap'):
        if flag == 'swap':
            requestURL = "https://www.ebi.ac.uk/QuickGO/services/ontology/go/search?query={}&limit=1&page=1".format(query)

        elif flag == 'child':
            requestURL = "https://www.ebi.ac.uk/QuickGO/services/ontology/go/terms/{}/children".format(query.replace(":","%3A"))

        try:
            r = requests.get(requestURL, headers={"Accept": "application/json"})
        except:
            return None
        if not r.ok:
            #r.raise_for_status()
            #sys.exit()
            return None
        responseBody = r.text
        #print(responseBody)
        goa = self.process_quickgo(responseBody,flag)
        return goa


    def process_quickgo(self,reponseBody,flag):
        reponseBody = json.loads(reponseBody)
        # swap negative & positive regulation
        if flag == 'swap':
            record = reponseBody["results"][0]
            if record["isObsolete"]:
                return None

            goa = GOA()
            goa.go_term = record["name"]
            goa.go_id = record["id"]
            goa.go_definition = record["definition"]["text"]
            return goa

        # replace with child go term
        elif flag == 'child':
            goa_list = list()
            record = reponseBody["results"][0]
            if "children" not in record.keys():
                return goa_list
            for child in record["children"]:
                if child["relation"] != "is_a":
                    continue # only replace the parent term with a child term in is_a relation

                goa = GOA()
                goa.go_term = child["name"]
                goa.go_id = child["id"]
                #goa.go_definition = child["definition"]["text"]
                goa_list.append(goa)
            return goa_list

class Brat:
    def __init__(self):
        self.spans = None
        self.type = None
        self.go_term = None
        self.go_id = None

    def fromstring(self,s):
        if not s:
            return None

        brat = Brat()
        for sub in s:
            sub = sub.split('\t')
            brat.type = sub[0]
            if 'T' in brat.type:
                brat.go_term = sub[2]
                brat.span = (int(sub[1].split(' ')[1]),int(sub[1].split(' ')[2]))
            elif 'N' in brat.type:
                brat.go_id = 'GO:'+sub[1].split('obo/GO_')[1]
        return brat

    def get_potential_go_ids(self,file):
        go_ids = set()
        file = '/Users/jiyuc/Documents/GitHub/bio/corpus/negatives/ucdenver-ccp-go/{}.a1'.format(file)
        with open(file,'r', encoding='utf-8') as fp:
            for line in fp:
                annotation = line.strip().split('\t')
                if 'N' in annotation[0]:
                    go_ids.add('GO:'+annotation[1].split('obo/GO_')[1])
                else:
                    continue
            fp.close()
        return go_ids


if __name__ == '__main__':
    GOA().query_go("negative regulation of feeding behavior")

