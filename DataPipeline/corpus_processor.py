import re

import enchant
import nltk
from nltk import SnowballStemmer
from nltk.tokenize import word_tokenize
from unidecode import unidecode

import DataPipeline.denoising_utility as du

nltk.download('stopwords')
nltk.download('punkt')

us_dict = enchant.Dict("en_US")
uk_dict = enchant.Dict("en_GB")


def processCorpus(corpus):
    stopwords = nltk.corpus.stopwords.words('english')
    param_stemmer = SnowballStemmer('english')

    for document in corpus:
        index = corpus.index(document)
        corpus[index] = corpus[index].replace(u'\ufffd', '8')  # Replaces the ASCII '�' symbol with '8'
        corpus[index] = corpus[index].replace(',', '')  # Removes commas
        corpus[index] = corpus[index].rstrip('\n')  # Removes line breaks
        corpus[index] = corpus[index].casefold()  # Makes all letters lowercase
        corpus[index] = re.sub(r'\W_', ' ', corpus[index])  # removes specials characters and leaves only words
        corpus[index] = re.sub(r"\S*\d\S*", " ", corpus[
            index])  # removes numbers and words concatenated with numbers IE h4ck3r. Removes road names such as BR-381.
        corpus[index] = re.sub(r"\S*@\S*\s?", " ", corpus[index])  # removes emails and mentions (words with @)
        corpus[index] = re.sub(r'http\S+', '', corpus[index])  # removes URLs with http
        corpus[index] = re.sub(r'www\S+', '', corpus[index])  # removes URLs with www
        corpus[index] = re.sub(r'\\r\\n[\s\S]*\\r\\n', '', corpus[index])  # removes code blocks
        corpus[index] = re.sub(":", '', corpus[index])  # removes URLs with www
        corpus[index] = re.sub('"', '', corpus[index])  # removes URLs with www
        corpus[index] = re.sub(",", '', corpus[index])  # removes URLs with www
        corpus[index] = re.sub("'", '', corpus[index])  # removes URLs with www
        corpus[index] = re.sub("//", '', corpus[index])  # removes URLs with www

        listOfTokens = word_tokenize(corpus[index])
        twoLetterWord = du.twoLetters(listOfTokens)

        listOfTokens = du.removeWords(listOfTokens, stopwords)
        listOfTokens = du.removeWords(listOfTokens, twoLetterWord)
        undict_words = []
        for word in listOfTokens:
            if not (us_dict.check(word) or uk_dict.check(word)):
                undict_words.append(word)

        listOfTokens = du.removeWords(listOfTokens, undict_words)
        listOfTokens = du.applyStemming(listOfTokens, param_stemmer)
        listOfTokens = du.removeWords(listOfTokens, stopwords)

        corpus[index] = " ".join(listOfTokens)
        corpus[index] = unidecode(corpus[index])

    return corpus


def processCorpusSingle(corpus):
    corpus = str(corpus)
    stopwords = nltk.corpus.stopwords.words('english')
    param_stemmer = SnowballStemmer('english')
    corpus = corpus.replace(u'\ufffd', '8')  # Replaces the ASCII '�' symbol with '8'
    corpus = corpus.replace(',', '')  # Removes commas
    corpus = corpus.rstrip('\n')  # Removes line breaks
    corpus = corpus.casefold()  # Makes all letters lowercase

    corpus = re.sub(r'\W_', ' ', corpus)  # removes specials characters and leaves only words
    corpus = re.sub(r"\S*\d\S*", " ",
                    corpus)  # removes numbers and words concatenated with numbers IE h4ck3r. Removes road names such as BR-381.
    corpus = re.sub(r"\S*@\S*\s?", " ", corpus)  # removes emails and mentions (words with @)
    corpus = re.sub(r'http\S+', '', corpus)  # removes URLs with http
    corpus = re.sub(r'www\S+', '', corpus)  # removes URLs with www
    corpus = re.sub(r'\\r\\n[\s\S]*\\r\\n', '', corpus)  # removes code blocks
    corpus = re.sub(r"`[\S\s]*?`", '', corpus)  # removes multiline code block
    corpus = re.sub(":", '', corpus)  # removes URLs with www
    corpus = re.sub('"', '', corpus)  # removes URLs with www
    corpus = re.sub(",", '', corpus)  # removes URLs with www
    corpus = re.sub("'", '', corpus)  # removes URLs with www
    corpus = re.sub("//", '', corpus)  # removes URLs with www

    listOfTokens = word_tokenize(corpus)
    twoLetterWord = du.twoLetters(listOfTokens)

    listOfTokens = du.removeWords(listOfTokens, stopwords)
    listOfTokens = du.removeWords(listOfTokens, twoLetterWord)
    undict_words = []
    for word in listOfTokens:
        if not (us_dict.check(word) or uk_dict.check(word)):
            undict_words.append(word)

    listOfTokens = du.removeWords(listOfTokens, undict_words)
    listOfTokens = du.applyStemming(listOfTokens, param_stemmer)
    listOfTokens = du.removeWords(listOfTokens, stopwords)

    corpus = " ".join(listOfTokens)
    corpus = unidecode(corpus)

    if corpus is None:
        print('None caught')

    return corpus
