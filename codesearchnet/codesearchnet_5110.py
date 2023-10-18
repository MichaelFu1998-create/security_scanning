def limit_sentences (path, word_limit=100):
    """
    iterator for the most significant sentences, up to a specified limit
    """
    word_count = 0

    if isinstance(path, str):
        path = json_iter(path)

    for meta in path:
        if not isinstance(meta, SummarySent):
            p = SummarySent(**meta)
        else:
            p = meta

        sent_text = p.text.strip().split(" ")
        sent_len = len(sent_text)

        if (word_count + sent_len) > word_limit:
            break
        else:
            word_count += sent_len
            yield sent_text, p.idx