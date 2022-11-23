import nltk
from nltk import tokenize
from operator import itemgetter
import math

from nltk.corpus import stopwords

def sent(word, sentences):
    f = [all([w in x for w in word]) for x in sentences]
    sl = [sentences[i] for i in range(0, len(f)) if f[i]]
    return int(len(sl))
def get_top_n(d, n):
    r = dict(sorted(d.items(), key = itemgetter(1), reverse = True)[:n])
    return r
def key(doc):
    nltk.download('stopwords')
    nltk.download('punkt')

    stop_words = set(stopwords.words('english'))
    total_sentences = tokenize.sent_tokenize(doc)
    total_sent_len = len(total_sentences)
    tf_score = {}
    total_words = doc.split()
    total_word_length = len(total_words)
    for each_word in total_words:
        each_word = each_word.replace('.', '')
        if each_word not in stop_words:
            if each_word in tf_score:
                tf_score[each_word] += 1
            else:
                tf_score[each_word] = 1

    # Dividing by total_word_length for each dictionary element
    tf_score.update((x, y / int(total_word_length)) for x, y in tf_score.items())
    idf_score = {}
    for each_word in total_words:
        each_word = each_word.replace('.', '')
        if each_word not in stop_words:
            if each_word in idf_score:
                idf_score[each_word] = sent(each_word, total_sentences)
            else:
                idf_score[each_word] = 1

    # Performing a log and divide
    idf_score.update((x, math.log(int(total_sent_len) / y)) for x, y in idf_score.items())
    tf_idf_score = {key: tf_score[key] * idf_score.get(key, 0) for key in tf_score.keys()}
    # getting top 3 results
    return list(get_top_n(tf_idf_score, 3).keys())