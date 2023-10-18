def random_string(length):
    '''
    Generate random string with parameter length.
    Example:

        >>> from eggit.egg_string import random_string
        >>> random_string(8)
        'q4f2eaT4'
        >>>

    '''

    str_list = [random.choice(string.digits + string.ascii_letters) for i in range(length)]
    return ''.join(str_list)