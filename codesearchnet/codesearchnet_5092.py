def fix_hypenation (foo):
    """
    fix hyphenation in the word list for a parsed sentence
    """
    i = 0
    bar = []

    while i < len(foo):
        text, lemma, pos, tag = foo[i]

        if (tag == "HYPH") and (i > 0) and (i < len(foo) - 1):
            prev_tok = bar[-1]
            next_tok = foo[i + 1]

            prev_tok[0] += "-" + next_tok[0]
            prev_tok[1] += "-" + next_tok[1]

            bar[-1] = prev_tok
            i += 2
        else:
            bar.append(foo[i])
            i += 1

    return bar