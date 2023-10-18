def merge_overlapping_in_list(l):
    '''Sorts list, merges any overlapping intervals, and also adjacent intervals. e.g.
       [0,1], [1,2] would be merge to [0,.2].'''
    i = 0
    l.sort()

    while i < len(l) - 1:
        u = l[i].union(l[i+1])
        if u is not None:
            l[i] = u
            l.pop(i+1)
        else:
            i += 1