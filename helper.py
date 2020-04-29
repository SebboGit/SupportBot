import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

stop_words = set(stopwords.words("english"))


def preprocess(sentence):
    sentence = sentence.lower()
    sentence = re.sub(r'[^\w\s]', '', sentence)
    tokens = word_tokenize(sentence)
    sentence = [i for i in tokens if i not in stop_words]
    return sentence


def compare(user_message, possible_response):
    similar_words = 0
    for word in user_message:
        if word in possible_response:
            similar_words += 1
    return similar_words


def get_similarity(tokens, category):
    output = []
    for token in tokens:
        output.append([token.text, category.text, token.similarity(category)])
    return output


def extract_nouns(sentence):
    """:arg sentence must be tagged with part of speech"""
    nouns = []
    for word in sentence:
        if word[1].startswith("N"):
            nouns.append(word[0])
    return nouns
