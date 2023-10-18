def remove_contained_in_list(l):
    '''Sorts list in place, then removes any intervals that are completely
       contained inside another interval'''
    i = 0
    l.sort()

    while i < len(l) - 1:
       if l[i+1].contains(l[i]):
           l.pop(i)
       elif l[i].contains(l[i+1]):
           l.pop(i+1)
       else:
           i += 1