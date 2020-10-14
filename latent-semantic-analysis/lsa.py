import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import TruncatedSVD
import pandas as pd
import numpy as np


def read_files(path):
    for root, dirnames, filenames in os.walk(path):
        for filename in filenames:
            path = os.path.join(root, filename)

            f = open(path, 'rt')
            text = f.read()
            f.close()

            yield text


def list_from_directory(path):
    l = []

    for text in read_files(path):
        l.append(text)

    return l


def remove_stop_words(sentence):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(sentence)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]

    return ' '.join(filtered_sentence)


body = list_from_directory('data')

body = [remove_stop_words(sentence) for sentence in body]

vectorizer = CountVectorizer()
bag_of_words = vectorizer.fit_transform(body)

svd = TruncatedSVD(n_components=2)
lsa = svd.fit_transform(bag_of_words)

topic_encoded_df = pd.DataFrame(lsa, columns=["topic_1", "topic_2"])
topic_encoded_df["body"] = body

dictionary = vectorizer.get_feature_names()

encoding_matrix = pd.DataFrame(svd.components_,
                               index=['topic_1', 'topic_2'],
                               columns=dictionary).T

encoding_matrix['abs_topic_1'] = np.abs(encoding_matrix['topic_1'])
encoding_matrix['abs_topic_2'] = np.abs(encoding_matrix['topic_2'])

encoding_matrix = encoding_matrix.sort_values('abs_topic_1', ascending=False)
print(encoding_matrix, 'Important Words - Topic 1')

encoding_matrix = encoding_matrix.sort_values('abs_topic_2', ascending=False)
print(encoding_matrix, 'Important Words - Topic 2')
