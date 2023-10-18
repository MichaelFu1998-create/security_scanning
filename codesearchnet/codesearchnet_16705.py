def reorder_list(source, targetorder):
    """Reorder a list to match target by moving a sequence at a time.

    Written for QtAbstractItemModel.moveRows.
    """
    i = 0
    while i < len(source):

        if source[i] == targetorder[i]:
            i += 1
            continue
        else:
            i0 = i
            j0 = source.index(targetorder[i0])
            j = j0 + 1
            while j < len(source):
                if source[j] == targetorder[j - j0 + i0]:
                    j += 1
                    continue
                else:
                    break
            move_elements(source, i0, j0, j - j0)
            i += j - j0