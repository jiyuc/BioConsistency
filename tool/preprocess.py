from textblob import TextBlob
def load_stopwords(stop_word_path):
    """
    This method will load NCBI created stopwords txt file into a set()

    :return: a set of stopwords
    """
    stop_words = set()
    with open(stop_word_path, 'r', encoding='utf-8') as rf:
        for line in rf:
            line = line.strip()
            stop_words.add(line)
    rf.close()
    return stop_words


def normalise(text):
    text = TextBlob(text)  # preprocessing using textblob
    text = [w.lemmatize('v').lower() for w in text.words]  # lemmatising verbs
    # stop_words = load_stopwords('')
    #text = [w for w in text if w not in stop_words] # remove stopwords
    return ' '.join(text)