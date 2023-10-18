def normalize_key_phrases (path, ranks, stopwords=None, spacy_nlp=None, skip_ner=True):
    """
    collect keyphrases, named entities, etc., while removing stop words
    """
    global STOPWORDS, SPACY_NLP

    # set up the stop words
    if (type(stopwords) is list) or (type(stopwords) is set):
        # explicit conversion to a set, for better performance
        stopwords = set(stopwords)
    else:
        if not STOPWORDS:
            STOPWORDS = load_stopwords(stopwords)

        stopwords = STOPWORDS

    # set up the spaCy NLP parser
    if not spacy_nlp:
        if not SPACY_NLP:
            SPACY_NLP = spacy.load("en")

        spacy_nlp = SPACY_NLP

    # collect keyphrases
    single_lex = {}
    phrase_lex = {}

    if isinstance(path, str):
        path = json_iter(path)

    for meta in path:
        sent = [w for w in map(WordNode._make, meta["graf"])]

        for rl in collect_keyword(sent, ranks, stopwords):
            id = str(rl.ids)

            if id not in single_lex:
                single_lex[id] = rl
            else:
                prev_lex = single_lex[id]
                single_lex[id] = rl._replace(count = prev_lex.count + 1)

        if not skip_ner:
            for rl in collect_entities(sent, ranks, stopwords, spacy_nlp):
                id = str(rl.ids)

                if id not in phrase_lex:
                    phrase_lex[id] = rl
                else:
                    prev_lex = phrase_lex[id]
                    phrase_lex[id] = rl._replace(count = prev_lex.count + 1)

        for rl in collect_phrases(sent, ranks, spacy_nlp):
            id = str(rl.ids)

            if id not in phrase_lex:
                phrase_lex[id] = rl
            else:
                prev_lex = phrase_lex[id]
                phrase_lex[id] = rl._replace(count = prev_lex.count + 1)

    # normalize ranks across single keywords and longer phrases:
    #    * boost the noun phrases based on their length
    #    * penalize the noun phrases for repeated words
    rank_list = [rl.rank for rl in single_lex.values()]

    if len(rank_list) < 1:
        max_single_rank = 0
    else:
        max_single_rank = max(rank_list)

    repeated_roots = {}

    for rl in sorted(phrase_lex.values(), key=lambda rl: len(rl), reverse=True):
        rank_list = []

        for i in iter(range(0, len(rl.ids))):
            id = rl.ids[i]

            if not id in repeated_roots:
                repeated_roots[id] = 1.0
                rank_list.append(rl.rank[i])
            else:
                repeated_roots[id] += 1.0
                rank_list.append(rl.rank[i] / repeated_roots[id])

        phrase_rank = calc_rms(rank_list)
        single_lex[str(rl.ids)] = rl._replace(rank = phrase_rank)

    # scale all the ranks together, so they sum to 1.0
    sum_ranks = sum([rl.rank for rl in single_lex.values()])

    for rl in sorted(single_lex.values(), key=lambda rl: rl.rank, reverse=True):
        if sum_ranks > 0.0:
            rl = rl._replace(rank=rl.rank / sum_ranks)
        elif rl.rank == 0.0:
            rl = rl._replace(rank=0.1)

        rl = rl._replace(text=re.sub(r"\s([\.\,\-\+\:\@])\s", r"\1", rl.text))
        yield rl