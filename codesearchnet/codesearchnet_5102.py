def collect_keyword (sent, ranks, stopwords):
    """
    iterator for collecting the single-word keyphrases
    """
    for w in sent:
        if (w.word_id > 0) and (w.root in ranks) and (w.pos[0] in "NV") and (w.root not in stopwords):
            rl = RankedLexeme(text=w.raw.lower(), rank=ranks[w.root]/2.0, ids=[w.word_id], pos=w.pos.lower(), count=1)

            if DEBUG:
                print(rl)

            yield rl