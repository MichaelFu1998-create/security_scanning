def _get_grammar_errors(self,pos,text,tokens):
        """
        Internal function to get the number of grammar errors in given text
        pos - part of speech tagged text (list)
        text - normal text (list)
        tokens - list of lists of tokenized text
        """
        word_counts = [max(len(t),1) for t in tokens]
        good_pos_tags = []
        min_pos_seq=2
        max_pos_seq=4
        bad_pos_positions=[]
        for i in xrange(0, len(text)):
            pos_seq = [tag[1] for tag in pos[i]]
            pos_ngrams = util_functions.ngrams(pos_seq, min_pos_seq, max_pos_seq)
            long_pos_ngrams=[z for z in pos_ngrams if z.count(' ')==(max_pos_seq-1)]
            bad_pos_tuples=[[z,z+max_pos_seq] for z in xrange(0,len(long_pos_ngrams)) if long_pos_ngrams[z] not in self._good_pos_ngrams]
            bad_pos_tuples.sort(key=operator.itemgetter(1))
            to_delete=[]
            for m in reversed(xrange(len(bad_pos_tuples)-1)):
                start, end = bad_pos_tuples[m]
                for j in xrange(m+1, len(bad_pos_tuples)):
                    lstart, lend = bad_pos_tuples[j]
                    if lstart >= start and lstart <= end:
                        bad_pos_tuples[m][1]=bad_pos_tuples[j][1]
                        to_delete.append(j)

            fixed_bad_pos_tuples=[bad_pos_tuples[z] for z in xrange(0,len(bad_pos_tuples)) if z not in to_delete]
            bad_pos_positions.append(fixed_bad_pos_tuples)
            overlap_ngrams = [z for z in pos_ngrams if z in self._good_pos_ngrams]
            if (len(pos_ngrams)-len(overlap_ngrams))>0:
                divisor=len(pos_ngrams)/len(pos_seq)
            else:
                divisor=1
            if divisor == 0:
                divisor=1
            good_grammar_ratio = (len(pos_ngrams)-len(overlap_ngrams))/divisor
            good_pos_tags.append(good_grammar_ratio)
        return good_pos_tags,bad_pos_positions