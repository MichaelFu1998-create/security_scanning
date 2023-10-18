def list_move_to_back(l,value='other'):
    """if the value is in the list, move it to the back and return it."""
    l=list(l)
    if value in l:
        l.remove(value)
        l.append(value)
    return l