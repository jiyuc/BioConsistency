import glob

def show_statistics(path):
    files = glob.glob(path)
    c = 0
    for filename in files:
        with open(filename,'r') as fp:
            for line in fp:
                c += 1
    print("number of instances",c)


if __name__ == '__main__':
    show_statistics('/Users/jiyuc/Documents/GitHub/bio/corpus/positives/*.txt')
    show_statistics('/Users/jiyuc/Documents/GitHub/bio/corpus/negatives/*.txt')