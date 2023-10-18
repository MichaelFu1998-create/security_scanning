def summarize(text, char_limit, sentence_filter=None, debug=False):
    '''
    select sentences in terms of maximum coverage problem

    Args:
      text: text to be summarized (unicode string)
      char_limit: summary length (the number of characters)

    Returns:
      list of extracted sentences

    Reference:
      Hiroya Takamura, Manabu Okumura.
      Text summarization model based on maximum coverage problem and its
      variant. (section 3)
      http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.222.6945
    '''
    debug_info = {}

    sents = list(tools.sent_splitter_ja(text))
    words_list = [
        # pulp variables should be utf-8 encoded
        w.encode('utf-8') for s in sents for w in tools.word_segmenter_ja(s)
    ]

    tf = collections.Counter()
    for words in words_list:
        for w in words:
            tf[w] += 1.0

    if sentence_filter is not None:
        valid_indices = [i for i, s in enumerate(sents) if sentence_filter(s)]
        sents = [sents[i] for i in valid_indices]
        words_list = [words_list[i] for i in valid_indices]

    sent_ids = [str(i) for i in range(len(sents))]  # sentence id
    sent_id2len = dict((id_, len(s)) for id_, s in zip(sent_ids, sents))  # c

    word_contain = dict()  # a
    for id_, words in zip(sent_ids, words_list):
        word_contain[id_] = collections.defaultdict(lambda: 0)
        for w in words:
            word_contain[id_][w] = 1

    prob = pulp.LpProblem('summarize', pulp.LpMaximize)

    # x
    sent_vars = pulp.LpVariable.dicts('sents', sent_ids, 0, 1, pulp.LpBinary)
    # z
    word_vars = pulp.LpVariable.dicts('words', tf.keys(), 0, 1, pulp.LpBinary)

    # first, set objective function: sum(w*z)
    prob += pulp.lpSum([tf[w] * word_vars[w] for w in tf])

    # next, add constraints
    # limit summary length: sum(c*x) <= K
    prob += pulp.lpSum(
        [sent_id2len[id_] * sent_vars[id_] for id_ in sent_ids]
    ) <= char_limit, 'lengthRequirement'
    # for each term, sum(a*x) <= z
    for w in tf:
        prob += pulp.lpSum(
            [word_contain[id_][w] * sent_vars[id_] for id_ in sent_ids]
        ) >= word_vars[w], 'z:{}'.format(w)

    prob.solve()
    # print("Status:", pulp.LpStatus[prob.status])

    sent_indices = []
    for v in prob.variables():
        # print v.name, "=", v.varValue
        if v.name.startswith('sents') and v.varValue == 1:
            sent_indices.append(int(v.name.split('_')[-1]))

    return [sents[i] for i in sent_indices], debug_info