def initialize_dictionaries(self, e_set, max_feats2 = 200):
        """
        Initializes dictionaries from an essay set object
        Dictionaries must be initialized prior to using this to extract features
        e_set is an input essay set
        returns a confirmation of initialization
        """
        if(hasattr(e_set, '_type')):
            if(e_set._type == "train"):
                #normal text (unstemmed) useful words/bigrams
                nvocab = util_functions.get_vocab(e_set._text, e_set._score, max_feats2 = max_feats2)
                #stemmed and spell corrected vocab useful words/ngrams
                svocab = util_functions.get_vocab(e_set._clean_stem_text, e_set._score, max_feats2 = max_feats2)
                #dictionary trained on proper vocab
                self._normal_dict = CountVectorizer(ngram_range=(1,2), vocabulary=nvocab)
                #dictionary trained on proper vocab
                self._stem_dict = CountVectorizer(ngram_range=(1,2), vocabulary=svocab)
                self.dict_initialized = True
                #Average spelling errors in set. needed later for spelling detection
                self._mean_spelling_errors=sum(e_set._spelling_errors)/float(len(e_set._spelling_errors))
                self._spell_errors_per_character=sum(e_set._spelling_errors)/float(sum([len(t) for t in e_set._text]))
                #Gets the number and positions of grammar errors
                good_pos_tags,bad_pos_positions=self._get_grammar_errors(e_set._pos,e_set._text,e_set._tokens)
                self._grammar_errors_per_character=(sum(good_pos_tags)/float(sum([len(t) for t in e_set._text])))
                #Generate bag of words features
                bag_feats=self.gen_bag_feats(e_set)
                #Sum of a row of bag of words features (topical words in an essay)
                f_row_sum=numpy.sum(bag_feats[:,:])
                #Average index of how "topical" essays are
                self._mean_f_prop=f_row_sum/float(sum([len(t) for t in e_set._text]))
                ret = "ok"
            else:
                raise util_functions.InputError(e_set, "needs to be an essay set of the train type.")
        else:
            raise util_functions.InputError(e_set, "wrong input. need an essay set object")
        return ret