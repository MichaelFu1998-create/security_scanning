def unique(seq):
    '''
    https://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-whilst-preserving-order
    '''
    has = []
    return [x for x in seq if not (x in has or has.append(x))]