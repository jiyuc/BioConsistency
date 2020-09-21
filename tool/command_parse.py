import argparse

def parse_command():
    parser = argparse.ArgumentParser(description='Generate Instance')
    parser.add_argument("--ann",type=str,help="file directory of bioc_annotation_xmls",required=True)
    parser.add_argument("--doc",type=str,help="file directory of bioc_doc_xmls",required=True)
    parser.add_argument("--out",type=str,help="file directory for storing generated instances",required=True)
    args = parser.parse_args()
    return args