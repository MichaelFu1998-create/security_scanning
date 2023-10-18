def collect_phrases (sent, ranks, spacy_nlp):
    """
    iterator for collecting the noun phrases
    """
    tail = 0
    last_idx = sent[0].idx - 1
    phrase = []

    while tail < len(sent):
        w = sent[tail]

        if (w.word_id > 0) and (w.root in ranks) and ((w.idx - last_idx) == 1):
            # keep collecting...
            rl = RankedLexeme(text=w.raw.lower(), rank=ranks[w.root], ids=w.word_id, pos=w.pos.lower(), count=1)
            phrase.append(rl)
        else:
            # just hit a phrase boundary
            for text, p in enumerate_chunks(phrase, spacy_nlp):
                if p:
                    id_list = [rl.ids for rl in p]
                    rank_list = [rl.rank for rl in p]
                    np_rl = RankedLexeme(text=text, rank=rank_list, ids=id_list, pos="np", count=1)

                    if DEBUG:
                        print(np_rl)

                    yield np_rl

            phrase = []

        last_idx = w.idx
        tail += 1