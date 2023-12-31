def load(fp, separator=DEFAULT, index_separator=DEFAULT, cls=dict, list_cls=list):
    '''Load an object from the file pointer.

    :param fp: A readable filehandle.
    :param separator: The separator between key and value.  Defaults to u'|' or b'|', depending on the types.
    :param index_separator: The separator between key and index.  Defaults to u'_' or b'_', depending on the types.
    :param cls: A callable that returns a Mapping that is filled with pairs.  The most common alternate option would be OrderedDict.
    :param list_cls: A callable that takes an iterable and returns a sequence.
    '''

    converter = None

    output = cls()
    arraykeys = set()

    for line in fp:
        if converter is None:
            if isinstance(line, six.text_type):
                converter = six.u
            else:
                converter = six.b
            default_separator = converter('|')
            default_index_separator = converter('_')
            newline = converter('\n')

            if separator is DEFAULT:
                separator = default_separator
            if index_separator is DEFAULT:
                index_separator = default_index_separator

        key, value = line.strip().split(separator, 1)

        keyparts = key.split(index_separator)

        try:
            index = int(keyparts[-1])
            endwithint = True
        except ValueError:
            endwithint = False

        # We do everything in-place to ensure that we maintain order when using
        # an OrderedDict.
        if len(keyparts) > 1 and endwithint:
            # If this is an array key
            basekey = key.rsplit(index_separator, 1)[0]
            if basekey not in arraykeys:
                arraykeys.add(basekey)

            if basekey in output:
                # If key already exists as non-array, fix it
                if not isinstance(output[basekey], dict):
                    output[basekey] = {-1: output[basekey]}
            else:
                output[basekey] = {}

            output[basekey][index] = value

        else:
            if key in output and isinstance(output[key], dict):
                output[key][-1] = value
            else:
                output[key] = value

    # Convert array keys
    for key in arraykeys:
        output[key] = list_cls(pair[1] for pair in sorted(six.iteritems(output[key])))

    return output