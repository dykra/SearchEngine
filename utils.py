from stemming.porter2 import stem
import re


def get_stop_words(stop_words_file):
    f = open(stop_words_file, 'r')
    stopwords = [line.rstrip() for line in f]
    stop_words = dict.fromkeys(stopwords)
    f.close()
    return stop_words


def format_text(f, stop_words_file=".././stopWordsFile.txt"):
    pattern = re.compile('[\W_]+')
    stop_words = get_stop_words(stop_words_file)
    f = pattern.sub(' ', f)
    re.sub(r'[\W_]+', '', f)
    f = [x for x in f.split() if x not in stop_words]
    f = [stem(word) for word in f]
    return f
