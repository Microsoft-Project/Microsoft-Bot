import re

import nltk
from nltk import SnowballStemmer
from nltk.tokenize import word_tokenize
from unidecode import unidecode

import denoising_utility

du = denoising_utility


def processCorpus(corpus, language):
    stopwords = nltk.corpus.stopwords.words(language)
    param_stemmer = SnowballStemmer(language)
    # countries_list =   # Load .txt file line by line

    for document in corpus:
        index = corpus.index(document)
        corpus[index] = corpus[index].replace(u'\ufffd', '8')  # Replaces the ASCII '�' symbol with '8'
        corpus[index] = corpus[index].replace(',', '')  # Removes commas
        corpus[index] = corpus[index].rstrip('\n')  # Removes line breaks
        corpus[index] = corpus[index].casefold()  # Makes all letters lowercase

        corpus[index] = re.sub('\W_', ' ', corpus[index])  # removes specials characters and leaves only words
        corpus[index] = re.sub("\S*\d\S*", " ", corpus[
            index])  # removes numbers and words concatenated with numbers IE h4ck3r. Removes road names such as BR-381.
        corpus[index] = re.sub("\S*@\S*\s?", " ", corpus[index])  # removes emails and mentions (words with @)
        corpus[index] = re.sub(r'http\S+', '', corpus[index])  # removes URLs with http
        corpus[index] = re.sub(r'www\S+', '', corpus[index])  # removes URLs with www

        corpus[index] = re.sub(":", '', corpus[index])  # removes URLs with www
        corpus[index] = re.sub('"', '', corpus[index])  # removes URLs with www
        corpus[index] = re.sub(",", '', corpus[index])  # removes URLs with www
        corpus[index] = re.sub("'", '', corpus[index])  # removes URLs with www
        corpus[index] = re.sub("//", '', corpus[index])  # removes URLs with www

        listOfTokens = word_tokenize(corpus[index])
        twoLetterWord = du.twoLetters(listOfTokens)

        listOfTokens = du.removeWords(listOfTokens, stopwords)
        listOfTokens = du.removeWords(listOfTokens, twoLetterWord)

        listOfTokens = du.applyStemming(listOfTokens, param_stemmer)
        # listOfTokens = applyStemming_dict(listOfTokens, param_stemmer)
        # listOfTokens = basic_stemming(listOfTokens)

        corpus[index] = " ".join(listOfTokens)
        corpus[index] = unidecode(corpus[index])

    return corpus
