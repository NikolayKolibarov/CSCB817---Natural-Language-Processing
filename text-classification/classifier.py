import os
import string
import nltk


def file_clean_tokenize(path):
    f = open(path, 'rt')
    text = f.read()
    f.close()

    tokens = nltk.word_tokenize(text)
    tokens = [token.lower() for token in tokens]

    punctuation = string.punctuation
    punctuation += '„“'
    punctuation += '–'
    table = str.maketrans('', '', punctuation)
    stripped = [token.translate(table) for token in tokens if token != ""]
    stripped = [token for token in stripped if token != ""]

    return stripped


def read_files(path):
    for root, dirnames, filenames in os.walk(path):
        for filename in filenames:
            path = os.path.join(root, filename)

            tokens = file_clean_tokenize(path)

            yield path, tokens


def list_from_directory(path):
    l = []

    for filename, message in read_files(path):
        l.append(message)

    return l[0]


university_words = list_from_directory('train/university')
pizza_words = list_from_directory('train/pizza')

university_bow = file_clean_tokenize('train/university-bow.txt')
pizza_bow = file_clean_tokenize('train/pizza-bow.txt')

count_all = len(set(university_words + pizza_words))

bow = university_bow + pizza_bow

university_word_probabilities = {}
pizza_word_probabilities = {}

for word in bow:
    count_university = university_words.count(word) + 1
    count_pizza = pizza_words.count(word) + 1

    university_word_probabilities[word] = count_university / (len(university_words) + count_all)
    pizza_word_probabilities[word] = count_pizza / (len(pizza_words) + count_all)


# test-1->pizza; test-2->university; test-3->university; test-4->pizza
test_words = file_clean_tokenize('test/test-1.txt')

university_probability = len(university_words) / (len(university_words) + len(pizza_words))
pizza_probability = len(pizza_words) / (len(pizza_words))

for word in test_words:
    word_probability_university = university_word_probabilities.get(word, 1)
    word_probability_pizza = pizza_word_probabilities.get(word, 1)

    university_probability *= word_probability_university
    pizza_probability *= word_probability_pizza

if university_probability > pizza_probability:
    print('UNIVERSITY')
else:
    print('PIZZA')
