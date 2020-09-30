import enchant

dictionary = enchant.Dict("en_US")


# removes a list of words (ie. stopwords) from a tokenized list.
def removeWords(listOfTokens, listOfWords):
    return [token for token in listOfTokens if token not in listOfWords]


# applies stemming to a list of tokenized words
def applyStemming(listOfTokens, stemmer):
    return [stemmer.stem(token) for token in listOfTokens]


def applyStemming_dict(listOfTokens, stemmer):
    list = []
    for token in listOfTokens:
        tmp = stemmer.stem(token)
        if dictionary.check(tmp):
            list.append(tmp)

    return list


# removes any words composed of less than 2 or more than 21 letters
def twoLetters(listOfTokens):
    twoLetterWord = []
    for token in listOfTokens:
        if len(token) <= 2 or len(token) >= 21:
            twoLetterWord.append(token)
    return twoLetterWord
