def __reconstruct(params):
    '''Reconstruct a transformation or pipeline given a parameter dump.'''

    if isinstance(params, dict):
        if '__class__' in params:
            cls = params['__class__']
            data = __reconstruct(params['params'])
            return cls(**data)
        else:
            data = dict()
            for key, value in six.iteritems(params):
                data[key] = __reconstruct(value)
            return data

    elif isinstance(params, (list, tuple)):
        return [__reconstruct(v) for v in params]

    else:
        return params