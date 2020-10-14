import re
from collections import Counter


def get_words(text):
    return re.findall(r'\w+', text.lower())


corpus = Counter(get_words(open('corpus.txt').read()))


def generate_words_edit_distance_one(word):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [left + right[1:] for left, right in splits if right]
    transposes = [left + right[1] + right[0] + right[2:] for left, right in splits if len(right) > 1]
    replaces = [left + character + right[1:] for left, right in splits if right for character in letters]
    inserts = [left + character + right for left, right in splits for character in letters]

    return set(deletes + transposes + replaces + inserts)


def generate_words_edit_distance_two(word):
    return (e2 for e1 in generate_words_edit_distance_one(word) for e2 in generate_words_edit_distance_one(e1))


def known(words):
    return set(word for word in words if word in corpus)


def probability(word, N=sum(corpus.values())):
    return corpus[word] / N


def candidates(word):
    return (known([word]) or known(generate_words_edit_distance_one(word)) or known(
        generate_words_edit_distance_two(word)) or [word])


def correction(word):
    return max(candidates(word), key=probability)


print(correction('tabel'))
print(correction('tatoo'))
print(correction('decishun'))

