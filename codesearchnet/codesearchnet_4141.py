def get_good_pos_ngrams(self):
        """
        Gets a set of gramatically correct part of speech sequences from an input file called essaycorpus.txt
        Returns the set and caches the file
        """
        if(os.path.isfile(NGRAM_PATH)):
            good_pos_ngrams = pickle.load(open(NGRAM_PATH, 'rb'))
        elif os.path.isfile(ESSAY_CORPUS_PATH):
            essay_corpus = open(ESSAY_CORPUS_PATH).read()
            essay_corpus = util_functions.sub_chars(essay_corpus)
            good_pos_ngrams = util_functions.regenerate_good_tokens(essay_corpus)
            pickle.dump(good_pos_ngrams, open(NGRAM_PATH, 'wb'))
        else:
            #Hard coded list in case the needed files cannot be found
            good_pos_ngrams=['NN PRP', 'NN PRP .', 'NN PRP . DT', 'PRP .', 'PRP . DT', 'PRP . DT NNP', '. DT',
             '. DT NNP', '. DT NNP NNP', 'DT NNP', 'DT NNP NNP', 'DT NNP NNP NNP', 'NNP NNP',
             'NNP NNP NNP', 'NNP NNP NNP NNP', 'NNP NNP NNP .', 'NNP NNP .', 'NNP NNP . TO',
             'NNP .', 'NNP . TO', 'NNP . TO NNP', '. TO', '. TO NNP', '. TO NNP NNP',
             'TO NNP', 'TO NNP NNP']

        return set(good_pos_ngrams)