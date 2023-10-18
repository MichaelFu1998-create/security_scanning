def _make_names_unique(animations):
    """
    Given a list of animations, some of which might have duplicate names, rename
    the first one to be <duplicate>_0, the second <duplicate>_1,
    <duplicate>_2, etc."""
    counts = {}
    for a in animations:
        c = counts.get(a['name'], 0) + 1
        counts[a['name']] = c
        if c > 1:
            a['name'] += '_' + str(c - 1)

    dupes = set(k for k, v in counts.items() if v > 1)
    for a in animations:
        if a['name'] in dupes:
            a['name'] += '_0'