def get_tiles (graf, size=3):
    """
    generate word pairs for the TextRank graph
    """
    keeps = list(filter(lambda w: w.word_id > 0, graf))
    keeps_len = len(keeps)

    for i in iter(range(0, keeps_len - 1)):
        w0 = keeps[i]

        for j in iter(range(i + 1, min(keeps_len, i + 1 + size))):
            w1 = keeps[j]

            if (w1.idx - w0.idx) <= size:
                yield (w0.root, w1.root,)