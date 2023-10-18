def _ensure_regexp(source, n):  #<- this function has to be improved
    '''returns True if regexp starts at n else returns False
      checks whether it is not a division '''
    markers = '(+~"\'=[%:?!*^|&-,;/\\'
    k = 0
    while True:
        k += 1
        if n - k < 0:
            return True
        char = source[n - k]
        if char in markers:
            return True
        if char != ' ' and char != '\n':
            break
    return False