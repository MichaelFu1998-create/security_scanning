def top_sentences (kernel, path):
    """
    determine distance for each sentence
    """
    key_sent = {}
    i = 0

    if isinstance(path, str):
        path = json_iter(path)

    for meta in path:
        graf = meta["graf"]
        tagged_sent = [WordNode._make(x) for x in graf]
        text = " ".join([w.raw for w in tagged_sent])

        m_sent = mh_digest([str(w.word_id) for w in tagged_sent])
        dist = sum([m_sent.jaccard(m) * rl.rank for rl, m in kernel])
        key_sent[text] = (dist, i)
        i += 1

    for text, (dist, i) in sorted(key_sent.items(), key=lambda x: x[1][0], reverse=True):
        yield SummarySent(dist=dist, idx=i, text=text)