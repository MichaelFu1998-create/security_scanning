def preprocess_dict(d):
    '''
    Preprocess a dict to be used as environment variables.

    :param d: dict to be processed
    '''

    out_env = {}
    for k, v in d.items():

        if not type(v) in PREPROCESSORS:
            raise KeyError('Invalid type in dict: {}'.format(type(v)))

        out_env[k] = PREPROCESSORS[type(v)](v)

    return out_env