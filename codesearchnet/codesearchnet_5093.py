def parse_graf (doc_id, graf_text, base_idx, spacy_nlp=None):
    """
    CORE ALGORITHM: parse and markup sentences in the given paragraph
    """
    global DEBUG
    global POS_KEEPS, POS_LEMMA, SPACY_NLP

    # set up the spaCy NLP parser
    if not spacy_nlp:
        if not SPACY_NLP:
            SPACY_NLP = spacy.load("en")

        spacy_nlp = SPACY_NLP

    markup = []
    new_base_idx = base_idx
    doc = spacy_nlp(graf_text, parse=True)

    for span in doc.sents:
        graf = []
        digest = hashlib.sha1()

        if DEBUG:
            print(span)

        # build a word list, on which to apply corrections
        word_list = []

        for tag_idx in range(span.start, span.end):
            token = doc[tag_idx]

            if DEBUG:
                print("IDX", tag_idx, token.text, token.tag_, token.pos_)
                print("reg", is_not_word(token.text))

            word_list.append([token.text, token.lemma_, token.pos_, token.tag_])

        # scan the parsed sentence, annotating as a list of `WordNode`
        corrected_words = fix_microsoft(fix_hypenation(word_list))

        for tok_text, tok_lemma, tok_pos, tok_tag in corrected_words:
            word = WordNode(word_id=0, raw=tok_text, root=tok_text.lower(), pos=tok_tag, keep=0, idx=new_base_idx)

            if is_not_word(tok_text) or (tok_tag == "SYM"):
                # a punctuation, or other symbol
                pos_family = '.'
                word = word._replace(pos=pos_family)
            else:
                pos_family = tok_tag.lower()[0]

            if pos_family in POS_LEMMA:
                # can lemmatize this word?
                word = word._replace(root=tok_lemma)

            if pos_family in POS_KEEPS:
                word = word._replace(word_id=get_word_id(word.root), keep=1)

            digest.update(word.root.encode('utf-8'))

            # schema: word_id, raw, root, pos, keep, idx
            if DEBUG:
                print(word)

            graf.append(list(word))
            new_base_idx += 1

        markup.append(ParsedGraf(id=doc_id, sha1=digest.hexdigest(), graf=graf))

    return markup, new_base_idx