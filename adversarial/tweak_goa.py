import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from obj.goa import GOA
import glob
from tqdm import tqdm
from obj.instance import Instance
import random
from tool.command_parse import parse_goa_command

def swap_go_regulation(instances):
    """
    This method will swap positive & negative regulation that appears in GOA
    to generate inconsistent GOA-evidence instances

    :param instances: a list of instances that required to be modified
    :return:a list of modified inconsistent instances
    """
    goa_process = GOA()
    visited = dict()
    processed = list()
    for instance in tqdm(instances):
        if "positive regulation" in instance.goa.go_term:
            query = instance.goa.go_term.replace("positive regulation","negative regulation")
        elif "negative regulation" in instance.goa.go_term:
            query = instance.goa.go_term.replace("negative","positive")
        else:
            continue # no keywords in go term, skip

        if query in visited: # go term in history
            instance.goa.go_term = query
            instance.goa.go_id = visited[query].goa.go_id
            instance.goa.go_definition = visited[query].goa.go_definition
        else:
            r = goa_process.query_go(query) # swap and query using quickgo api
            instance.goa.go_term = r.go_term
            instance.goa.go_id = r.go_id
            instance.goa.go_definition = r.go_definition
            visited[query] = instance # save in history
        processed.append(instance)
    return processed

def evidence2go_index(instances):
    """
    This method construct a index (key) raw text of evidence; (value) a list of associated GO ids
    :param instances: a list of GOA-evidence instances
    :return: evidence2go indexb
    """
    e2go_index = dict()
    for instance in instances:
        evidence_text = instance.evidence.text
        go_id = instance.goa.go_id
        e2go_index[evidence_text] = e2go_index.get(evidence_text,[]) + [go_id]
    return e2go_index

def select_go_child(children, ignore):
    if not children or len(children) == 0:
        return None
    
    # uncomment following line of code to apply training set optimisation strategy
    #children = sorted([(count_go_term_overlap(node,child),child) for child in children],key=lambda x:x[0], reverse=False)

    random.shuffle(children) # comment this line when applying training set optimisation strategy
    for child in children:
        if child not in ignore:
            return child
        else:
            continue
    return None

def count_go_term_overlap(term1, term2):
    term1 = set(term1.split(' '))
    #print(term2.go_term)
    term2 = set(term2.go_term.split(' '))
    distance = len(term1-term2)
    return distance


def replace_with_go_child(instances):
    e2go_index = evidence2go_index(instances)
    visited = dict() # reduce time to query QuickGO
    processed = list() # save go_term replaced instances
    for instance in tqdm(instances):
        go_id = instance.goa.go_id
        if go_id in visited:
            selected_child = select_go_child(visited.get(go_id),e2go_index.get(instance.evidence.text))
        else:
            children = GOA().query_go(instance.goa.go_id,'child')
            visited[go_id] = children
            selected_child = select_go_child(children,e2go_index.get(instance.evidence.text))
        if not selected_child:
            continue
        instance.goa.go_id = selected_child.go_id
        instance.goa.go_term = selected_child.go_term
        processed.append(instance)
    return processed

def select_evidence_code(instance):
    """
    This method replace evidence code in an instance according to
    https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3220872/

    :param instance: a consistent GOA-Evidence instance
    :return: a modified inconsistent GOA-Evidence instance, or None (if unsuccessful)
    """
    if not instance:
        return None

    evidence = instance.goa.evidence_code
    exp_codes = ['EXP','IMP','IGI','IPI','IDA','IEP']
    if evidence not in exp_codes:
        return None

    if evidence == 'EXP':
        instance.goa.evidence_code = random.choice(exp_codes[1:])
    elif evidence == 'IMP':
        instance.goa.evidence_code = random.choice(exp_codes[2:])
    elif evidence == 'IGI':
        instance.goa.evidence_code = random.choice(exp_codes[3:])
    elif evidence == 'IPI':
        instance.goa.evidence_code = random.choice(exp_codes[4:])
    elif evidence == 'IDA':
        instance.goa.evidence_code = random.choice(exp_codes[5:])
    elif evidence == 'IEP': # bottom of decision tree, do not modify
        return None
    return instance



def replace_exp_evidence_code(instances):
    """
    This rule modify experimental typed evidence code in TPs to form negatives

    :param instances: a list of TP instances
    :return: a list of evidence_code modified negatives
    """
    processed = list()
    for instance in instances:
        instance = select_evidence_code(instance)
        if not instance:
            continue

        processed.append(instance)
    return processed


def save_processed_totxt(processed,file_directory):
    if not processed:
        return

    for instance in tqdm(processed):
        docid = instance.evidence.docid
        filename = file_directory.format(docid)
        f = open(filename,'a',encoding='utf-8')
        f.write(instance.tostring())
        f.close()
    print("directory location:{}".format(file_directory))

if __name__ == '__main__':

    args = parse_goa_command()
    positive_document_path = args.pos+'*.txt'
    swapped_negative_path = args.swap
    go_replaced_negative_path = args.specificity
    ec_replaced_negative_path = args.evicode

    instances = list()
    pos_files = glob.glob(positive_document_path)
    # load positives instances
    for pos_filename in tqdm(pos_files):
        with open(pos_filename, 'r') as fp:
            for line in fp:
                instances.append(Instance().fromstring(line))

    # swap positive & negative regulations in go terms
    processes = swap_go_regulation(instances)

    # save the swapped instance as negatives
    save_processed_totxt(processes,swapped_negative_path)

    # replace go term with child term
    processes = replace_with_go_child(instances)

    # save go replaced instances as negatives
    save_processed_totxt(processes,go_replaced_negative_path)

    # replace evidence code according to decision tree
    processes = replace_exp_evidence_code(instances)

    # save evidence code replaced instances as negatives
    save_processed_totxt(processes,ec_replaced_negative_path)
