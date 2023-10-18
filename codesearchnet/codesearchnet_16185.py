def guess_header(array, name=''):
    """Guess the array header information.
    Returns a header dict, with class, data type, and size information.
    """
    header = {}

    if isinstance(array, Sequence) and len(array) == 1:
        # sequence with only one element, squeeze the array
        array = array[0]

    if isinstance(array, basestring):
        header.update({
            'mclass': 'mxCHAR_CLASS', 'mtp': 'miUTF8',
            'dims': (1 if len(array) > 0 else 0, len(array))})

    elif isinstance(array, Sequence) and len(array) == 0:
        # empty (int) array
        header.update({
            'mclass': 'mxINT32_CLASS', 'mtp': 'miINT32', 'dims': (0, 0)})

    elif isinstance(array, Mapping):
        # test if cells (values) of all fields are of equal type and
        # have equal length
        field_types = [type(j) for j in array.values()]
        field_lengths = [1 if isinstance(j, (basestring, int, float))
                         else len(j) for j in array.values()]
        if len(field_lengths) == 1:
            equal_lengths = True
            equal_types = True
        else:
            equal_lengths = not any(diff(field_lengths))
            equal_types = all([field_types[0] == f for f in field_types])

        # if of unqeual lengths or unequal types, then treat each value
        # as a cell in a 1x1 struct
        header.update({
            'mclass': 'mxSTRUCT_CLASS',
            'dims': (
                1,
                field_lengths[0] if equal_lengths and equal_types else 1)}
            )

    elif isinstance(array, int):
        header.update({
            'mclass': 'mxINT32_CLASS', 'mtp': 'miINT32', 'dims': (1, 1)})

    elif isinstance(array, float):
        header.update({
            'mclass': 'mxDOUBLE_CLASS', 'mtp': 'miDOUBLE', 'dims': (1, 1)})

    elif isinstance(array, Sequence):

        if isarray(array, lambda i: isinstance(i, int), 1):
            # 1D int array
            header.update({
                'mclass': 'mxINT32_CLASS', 'mtp': 'miINT32',
                'dims': (1, len(array))})

        elif isarray(array, lambda i: isinstance(i, (int, float)), 1):
            # 1D double array
            header.update({
                'mclass': 'mxDOUBLE_CLASS', 'mtp': 'miDOUBLE',
                'dims': (1, len(array))})

        elif (isarray(array, lambda i: isinstance(i, Sequence), 1) and
                any(diff(len(s) for s in array))):
            # sequence of unequal length, assume cell array
            header.update({
                'mclass': 'mxCELL_CLASS',
                'dims': (1, len(array))
            })

        elif isarray(array, lambda i: isinstance(i, basestring), 1):
            # char array
            header.update({
                'mclass': 'mxCHAR_CLASS', 'mtp': 'miUTF8',
                'dims': (len(array), len(array[0]))})

        elif isarray(array, lambda i: isinstance(i, Sequence), 1):
            # 2D array

            if any(diff(len(j) for j in array)):
                # rows are of unequal length, make it a cell array
                header.update({
                    'mclass': 'mxCELL_CLASS',
                    'dims': (len(array), len(array[0]))})

            elif isarray(array, lambda i: isinstance(i, int)):
                # 2D int array
                header.update({
                    'mclass': 'mxINT32_CLASS', 'mtp': 'miINT32',
                    'dims': (len(array), len(array[0]))})

            elif isarray(array, lambda i: isinstance(i, (int, float))):
                # 2D double array
                header.update({
                    'mclass': 'mxDOUBLE_CLASS',
                    'mtp': 'miDOUBLE',
                    'dims': (len(array), len(array[0]))})

        elif isarray(array, lambda i: isinstance(
                i, (int, float, basestring, Sequence, Mapping))):
            # mixed contents, make it a cell array
            header.update({
                'mclass': 'mxCELL_CLASS',
                'dims': (1, len(array))})

    if not header:
        raise ValueError(
            'Only dicts, two dimensional numeric, '
            'and char arrays are currently supported')
    header['name'] = name
    return header, array