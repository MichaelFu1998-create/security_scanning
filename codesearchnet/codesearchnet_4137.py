def get_separator_words(toks1):
    """
    Finds the words that separate a list of tokens from a background corpus
    Basically this generates a list of informative/interesting words in a set
    toks1 is a list of words
    Returns a list of separator words
    """
    tab_toks1 = nltk.FreqDist(word.lower() for word in toks1)
    if(os.path.isfile(ESSAY_COR_TOKENS_PATH)):
        toks2 = pickle.load(open(ESSAY_COR_TOKENS_PATH, 'rb'))
    else:
        essay_corpus = open(ESSAY_CORPUS_PATH).read()
        essay_corpus = sub_chars(essay_corpus)
        toks2 = nltk.FreqDist(word.lower() for word in nltk.word_tokenize(essay_corpus))
        pickle.dump(toks2, open(ESSAY_COR_TOKENS_PATH, 'wb'))
    sep_words = []
    for word in tab_toks1.keys():
        tok1_present = tab_toks1[word]
        if(tok1_present > 2):
            tok1_total = tab_toks1._N
            tok2_present = toks2[word]
            tok2_total = toks2._N
            fish_val = pvalue(tok1_present, tok2_present, tok1_total, tok2_total).two_tail
            if(fish_val < .001 and tok1_present / float(tok1_total) > (tok2_present / float(tok2_total)) * 2):
                sep_words.append(word)
    sep_words = [w for w in sep_words if not w in nltk.corpus.stopwords.words("english") and len(w) > 5]
    return sep_words