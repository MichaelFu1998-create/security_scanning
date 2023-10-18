def unflatten(master):
    """
    :param dict master: a multilevel dictionary
    :return: a unflattened dictionary
    :rtype: dict

    Unflattens a single-level dictionary a multilevel into one so that::

        {'foo.bar.a': 1,
         'foo.bar.b': True,
         'foo.bar.a': 1,
         }

    would become::

        {'foo':
            {'bar':
               {
                   'a': 1,
                   'b': True,
                   'c': 'hello',
                },
            },
        }
    """
    result = {}

    for k, v in master.items():
        *first, last = k.split('.')
        r = result
        for i in first:
            r = r.setdefault(i, {})
        r[last] = v

    return result