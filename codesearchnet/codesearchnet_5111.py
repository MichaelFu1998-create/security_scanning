def make_sentence (sent_text):
    """
    construct a sentence text, with proper spacing
    """
    lex = []
    idx = 0

    for word in sent_text:
        if len(word) > 0:
            if (idx > 0) and not (word[0] in ",.:;!?-\"'"):
                lex.append(" ")

            lex.append(word)

        idx += 1

    return "".join(lex)