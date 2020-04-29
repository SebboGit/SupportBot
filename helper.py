import re
from collections import Counter
import spacy
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nlp = spacy.load("en")
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