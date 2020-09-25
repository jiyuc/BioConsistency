import argparse

def parse_command():
    parser = argparse.ArgumentParser(description='Generate Instance')
    parser.add_argument("--ann",type=str,help="file directory of bioc_annotation_xmls",required=True)
    parser.add_argument("--doc",type=str,help="file directory of bioc_doc_xmls",required=True)
    parser.add_argument("--out",type=str,help="file directory for storing generated instances",required=True)
    args = parser.parse_args()
    return args

def parse_retrieval_command():
    parser = argparse.ArgumentParser(description='Retrieve TN as negatives')
    parser.add_argument("--pos", type=str, help="file directory of splitted positives *.txt", required=True)
    parser.add_argument("--model", type=str, help="pre-trained sent2vec model *.bin", required=True)
    parser.add_argument("--out", type=str, help="file directory for storing generated instances", required=True)
    args = parser.parse_args()
    return args

def parse_goa_command():
    parser = argparse.ArgumentParser(description='Retrieve TN as negatives')
    parser.add_argument("--pos", type=str, help="file directory of splitted positives *.txt", required=True)
    parser.add_argument("--swap", type=str, help="file directory of GO swapped negatives *.txt", required=True)
    parser.add_argument("--specificity", type=str, help="file directory of GO specificity modified negatives", required=True)
    parser.add_argument("--evicode", type=str, help="file directory of GO evidence code modified negatives", required=True)
    args = parser.parse_args()
    return args
