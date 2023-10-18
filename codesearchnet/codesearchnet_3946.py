def parse_generator_doubling(config):
    """ Returns generators that double with each value returned
        Config includes optional start value """
    start = 1
    if 'start' in config:
        start = int(config['start'])

    # We cannot simply use start as the variable, because of scoping
    # limitations
    def generator():
        val = start
        while(True):
            yield val
            val = val * 2
    return generator()