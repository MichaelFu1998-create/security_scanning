def join_dicts(*dicts):
    '''Join a bunch of dicts'''

    out_dict = {}

    for d in dicts:
        for k, v in d.iteritems():

            if not type(v) in JOINERS:
                raise KeyError('Invalid type in dict: {}'.format(type(v)))

            JOINERS[type(v)](out_dict, k, v)

    return out_dict