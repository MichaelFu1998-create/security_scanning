def printoptions():
    '''print paver options.

    Prettified by json.
    `long_description` is removed
    '''
    x = json.dumps(environment.options,
                   indent=4,
                   sort_keys=True,
                   skipkeys=True,
                   cls=MyEncoder)
    print(x)