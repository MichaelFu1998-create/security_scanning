def edit_distance(s1, s2):
    """
    Calculates string edit distance between string 1 and string 2.
    Deletion, insertion, substitution, and transposition all increase edit distance.
    """
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    for i in xrange(-1, lenstr1 + 1):
        d[(i, -1)] = i + 1
    for j in xrange(-1, lenstr2 + 1):
        d[(-1, j)] = j + 1

    for i in xrange(lenstr1):
        for j in xrange(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i, j)] = min(
                d[(i - 1, j)] + 1, # deletion
                d[(i, j - 1)] + 1, # insertion
                d[(i - 1, j - 1)] + cost, # substitution
            )
            if i and j and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + cost) # transposition

    return d[lenstr1 - 1, lenstr2 - 1]