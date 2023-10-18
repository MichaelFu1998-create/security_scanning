def generate_additional_essays(self, e_text, e_score, dictionary=None, max_syns=3):
        """
        Substitute synonyms to generate extra essays from existing ones.
        This is done to increase the amount of training data.
        Should only be used with lowest scoring essays.
        e_text is the text of the original essay.
        e_score is the score of the original essay.
        dictionary is a fixed dictionary (list) of words to replace.
        max_syns defines the maximum number of additional essays to generate.  Do not set too high.
        """
        e_toks = nltk.word_tokenize(e_text)
        all_syns = []
        for word in e_toks:
            synonyms = util_functions.get_wordnet_syns(word)
            if(len(synonyms) > max_syns):
                synonyms = random.sample(synonyms, max_syns)
            all_syns.append(synonyms)
        new_essays = []
        for i in range(0, max_syns):
            syn_toks = e_toks
            for z in range(0, len(e_toks)):
                if len(all_syns[z]) > i and (dictionary == None or e_toks[z] in dictionary):
                    syn_toks[z] = all_syns[z][i]
            new_essays.append(" ".join(syn_toks))
        for z in xrange(0, len(new_essays)):
            self.add_essay(new_essays[z], e_score, 1)