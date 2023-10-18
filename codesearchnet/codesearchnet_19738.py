def const_equal(str_a, str_b):
    '''Constant time string comparison'''

    if len(str_a) != len(str_b):
        return False

    result = True
    for i in range(len(str_a)):
        result &= (str_a[i] == str_b[i])

    return result