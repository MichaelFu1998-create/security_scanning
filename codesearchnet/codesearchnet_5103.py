def collect_entities (sent, ranks, stopwords, spacy_nlp):
    """
    iterator for collecting the named-entities
    """
    global DEBUG
    sent_text = " ".join([w.raw for w in sent])

    if DEBUG:
        print("sent:", sent_text)

    for ent in spacy_nlp(sent_text).ents:
        if DEBUG:
            print("NER:", ent.label_, ent.text)

        if (ent.label_ not in ["CARDINAL"]) and (ent.text.lower() not in stopwords):
            w_ranks, w_ids = find_entity(sent, ranks, ent.text.split(" "), 0)

            if w_ranks and w_ids:
                rl = RankedLexeme(text=ent.text.lower(), rank=w_ranks, ids=w_ids, pos="np", count=1)

                if DEBUG:
                    print(rl)

                yield rl