def pairwise(iterable: Iterable[X]) -> Iterable[Tuple[X, X]]:
    """Iterate over pairs in list s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = itt.tee(iterable)
    next(b, None)
    return zip(a, b)