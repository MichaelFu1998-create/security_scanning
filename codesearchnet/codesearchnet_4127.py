def get_vocab(text, score, max_feats=750, max_feats2=200):
    """
    Uses a fisher test to find words that are significant in that they separate
    high scoring essays from low scoring essays.
    text is a list of input essays.
    score is a list of scores, with score[n] corresponding to text[n]
    max_feats is the maximum number of features to consider in the first pass
    max_feats2 is the maximum number of features to consider in the second (final) pass
    Returns a list of words that constitute the significant vocabulary
    """
    dict = CountVectorizer(ngram_range=(1,2), max_features=max_feats)
    dict_mat = dict.fit_transform(text)
    set_score = numpy.asarray(score, dtype=numpy.int)
    med_score = numpy.median(set_score)
    new_score = set_score
    if(med_score == 0):
        med_score = 1
    new_score[set_score < med_score] = 0
    new_score[set_score >= med_score] = 1

    fish_vals = []
    for col_num in range(0, dict_mat.shape[1]):
        loop_vec = dict_mat.getcol(col_num).toarray()
        good_loop_vec = loop_vec[new_score == 1]
        bad_loop_vec = loop_vec[new_score == 0]
        good_loop_present = len(good_loop_vec[good_loop_vec > 0])
        good_loop_missing = len(good_loop_vec[good_loop_vec == 0])
        bad_loop_present = len(bad_loop_vec[bad_loop_vec > 0])
        bad_loop_missing = len(bad_loop_vec[bad_loop_vec == 0])
        fish_val = pvalue(good_loop_present, bad_loop_present, good_loop_missing, bad_loop_missing).two_tail
        fish_vals.append(fish_val)

    cutoff = 1
    if(len(fish_vals) > max_feats2):
        cutoff = sorted(fish_vals)[max_feats2]
    good_cols = numpy.asarray([num for num in range(0, dict_mat.shape[1]) if fish_vals[num] <= cutoff])

    getVar = lambda searchList, ind: [searchList[i] for i in ind]
    vocab = getVar(dict.get_feature_names(), good_cols)

    return vocab