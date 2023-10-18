def gen_feedback(self, e_set, features=None):
        """
        Generate feedback for a given set of essays
        e_set - EssaySet object
        features - optionally, pass in a matrix of features extracted from e_set using FeatureExtractor
        in order to get off topic feedback.
        Returns a list of lists (one list per essay in e_set)
        e_set - EssaySet object
        """

        #Set ratio to modify thresholds for grammar/spelling errors
        modifier_ratio=1.05

        #Calc number of grammar and spelling errors per character
        set_grammar,bad_pos_positions=self._get_grammar_errors(e_set._pos,e_set._text,e_set._tokens)
        set_grammar_per_character=[set_grammar[m]/float(len(e_set._text[m])+.1) for m in xrange(0,len(e_set._text))]
        set_spell_errors_per_character=[e_set._spelling_errors[m]/float(len(e_set._text[m])+.1) for m in xrange(0,len(e_set._text))]

        #Iterate through essays and create a feedback dict for each
        all_feedback=[]
        for m in xrange(0,len(e_set._text)):
            #Be very careful about changing these messages!
            individual_feedback={'grammar' : "Grammar: Ok.",
                                 'spelling' : "Spelling: Ok.",
                                 'markup_text' : "",
                                 'grammar_per_char' : set_grammar_per_character[m],
                                 'spelling_per_char' : set_spell_errors_per_character[m],
                                 'too_similar_to_prompt' : False,
                                 }
            markup_tokens=e_set._markup_text[m].split(" ")

            #This loop ensures that sequences of bad grammar get put together into one sequence instead of staying
            #disjointed
            bad_pos_starts=[z[0] for z in bad_pos_positions[m]]
            bad_pos_ends=[z[1]-1 for z in bad_pos_positions[m]]
            for z in xrange(0,len(markup_tokens)):
                if z in bad_pos_starts:
                    markup_tokens[z]='<bg>' + markup_tokens[z]
                elif z in bad_pos_ends:
                    markup_tokens[z]=markup_tokens[z] + "</bg>"
            if(len(bad_pos_ends)>0 and len(bad_pos_starts)>0 and len(markup_tokens)>1):
                if max(bad_pos_ends)>(len(markup_tokens)-1) and max(bad_pos_starts)<(len(markup_tokens)-1):
                    markup_tokens[len(markup_tokens)-1]+="</bg>"

            #Display messages if grammar/spelling errors greater than average in training set
            if set_grammar_per_character[m]>(self._grammar_errors_per_character*modifier_ratio):
                individual_feedback['grammar']="Grammar: More grammar errors than average."
            if set_spell_errors_per_character[m]>(self._spell_errors_per_character*modifier_ratio):
                individual_feedback['spelling']="Spelling: More spelling errors than average."

            #Test topicality by calculating # of on topic words per character and comparing to the training set
            #mean.  Requires features to be passed in
            if features is not None:
                f_row_sum=numpy.sum(features[m,12:])
                f_row_prop=f_row_sum/len(e_set._text[m])
                if f_row_prop<(self._mean_f_prop/1.5) or len(e_set._text[m])<20:
                    individual_feedback['topicality']="Topicality: Essay may be off topic."

                if(features[m,9]>.6):
                    individual_feedback['prompt_overlap']="Prompt Overlap: Too much overlap with prompt."
                    individual_feedback['too_similar_to_prompt']=True
                    log.debug(features[m,9])

            #Create string representation of markup text
            markup_string=" ".join(markup_tokens)
            individual_feedback['markup_text']=markup_string
            all_feedback.append(individual_feedback)

        return all_feedback