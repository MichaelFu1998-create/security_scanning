def flatten(master):
    """
    :param dict master: a multilevel dictionary
    :return: a flattened dictionary
    :rtype: dict

    Flattens a multilevel dictionary into a single-level one so that::

        {'foo':
            {'bar':
               {
                   'a': 1,
                   'b': True,
                   'c': 'hello',
                },
            },
        }

    would become::

        {'foo.bar.a': 1,
         'foo.bar.b': True,
         'foo.bar.a': 1,
         }

    You can mix and match both input (hierarchical) and output (dotted) formats
    in the input without problems - and if you call flatten more than once, it
    has no effect.
    """
    result = {}

    def add(value, *keys):
        if keys in result:
            raise ValueError('Duplicate key %s' % keys)
        result[keys] = value

    def recurse(value, *keys):
        if isinstance(value, dict):
            for k, v in value.items():
                recurse(v, k, *keys)
        else:
            key = '.'.join(reversed(keys))
            if key in result:
                raise ValueError('Duplicate key %s' % str(keys))
            result[key] = value

    recurse(master)
    return result