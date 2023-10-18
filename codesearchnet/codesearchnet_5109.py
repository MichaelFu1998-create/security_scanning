def limit_keyphrases (path, phrase_limit=20):
    """
    iterator for the most significant key phrases
    """
    rank_thresh = None

    if isinstance(path, str):
        lex = []

        for meta in json_iter(path):
            rl = RankedLexeme(**meta)
            lex.append(rl)
    else:
        lex = path

    if len(lex) > 0:
        rank_thresh = statistics.mean([rl.rank for rl in lex])
    else:
            rank_thresh = 0

    used = 0

    for rl in lex:
        if rl.pos[0] != "v":
            if (used > phrase_limit) or (rl.rank < rank_thresh):
                return

            used += 1
            yield rl.text.replace(" - ", "-")