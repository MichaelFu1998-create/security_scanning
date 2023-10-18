def rank_kernel (path):
    """
    return a list (matrix-ish) of the key phrases and their ranks
    """
    kernel = []

    if isinstance(path, str):
        path = json_iter(path)

    for meta in path:
        if not isinstance(meta, RankedLexeme):
            rl = RankedLexeme(**meta)
        else:
            rl = meta

        m = mh_digest(map(lambda x: str(x), rl.ids))
        kernel.append((rl, m,))

    return kernel