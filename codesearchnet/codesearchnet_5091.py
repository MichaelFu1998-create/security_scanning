def fix_microsoft (foo):
    """
    fix special case for `c#`, `f#`, etc.; thanks Microsoft
    """
    i = 0
    bar = []

    while i < len(foo):
        text, lemma, pos, tag = foo[i]

        if (text == "#") and (i > 0):
            prev_tok = bar[-1]

            prev_tok[0] += "#"
            prev_tok[1] += "#"

            bar[-1] = prev_tok
        else:
            bar.append(foo[i])

        i += 1

    return bar