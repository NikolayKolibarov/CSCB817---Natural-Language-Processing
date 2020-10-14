import string
import nltk

# load text
f = open('sentences.txt', 'rt')
text = f.read()
f.close()

# split into sentences
sentences = nltk.sent_tokenize(text, "english")
print(sentences[:10])

# insert <BEGIN> and <END> tags for beginning and ending of sentences
sentences = ["<BEGIN> " + sentence + " <END> " for sentence in sentences]
print(sentences[:10])

# split into tokens by whitespace
tokens = "".join(sentences).split()
print(tokens[:100])

# convert to lowercase
tokens = [token.lower() for token in tokens]

search_str = "<BEGIN> I love you".lower()
search_list = search_str.split()

probabilities_list = list()
for i in range(1, len(search_list)):
    currentSearchToken = search_list[i - 1]
    nextSearchToken = search_list[i]
    tokenSequenceCounter = 0
    tokenCounter = 0
    for j in range(1, len(tokens)):
        currentTextToken = tokens[j - 1]
        nextTextToken = tokens[j]

        if currentSearchToken == currentTextToken and nextSearchToken == nextTextToken:
            tokenSequenceCounter += 1

        if currentSearchToken == currentTextToken:
            tokenCounter += 1

    conditional_probability = (tokenSequenceCounter + 1) / (tokenCounter + len(tokens))
    probabilities_list.append(conditional_probability)

    print(currentSearchToken, '//curr search token')
    print(nextSearchToken, '//next search token')
    print(tokenSequenceCounter, '//token seq counter')
    print(tokenCounter, '//token counter')

print(probabilities_list)

probabilities_product = 1
for probability in probabilities_list:
    probabilities_product *= probability

print(probabilities_product, '// Probability of occurring "I love you" in corpus')
