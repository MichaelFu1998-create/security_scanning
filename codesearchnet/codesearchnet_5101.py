def enumerate_chunks (phrase, spacy_nlp):
    """
    iterate through the noun phrases
    """
    if (len(phrase) > 1):
        found = False
        text = " ".join([rl.text for rl in phrase])
        doc = spacy_nlp(text.strip(), parse=True)

        for np in doc.noun_chunks:
            if np.text != text:
                found = True
                yield np.text, find_chunk(phrase, np.text.split(" "))

        if not found and all([rl.pos[0] != "v" for rl in phrase]):
            yield text, phrase