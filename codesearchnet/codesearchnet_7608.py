def _parse_dict_recursive(dict_str):
    """Parse a dictionary from the search index"""
    dict_out = dict()
    pos_last = 0
    pos = dict_str.find(':')
    while pos >= 0:
        key = dict_str[pos_last:pos]
        if dict_str[pos + 1] == '[':
            # value is a list
            pos_tmp = dict_str.find(']', pos + 1)
            if pos_tmp < 0:
                raise RuntimeError('error when parsing dict')
            value = dict_str[pos + 2: pos_tmp].split(',')
            # try to convert elements to int
            for i in range(len(value)):
                try:
                    value[i] = int(value[i])
                except ValueError:
                    pass
        elif dict_str[pos + 1] == '{':
            # value is another dictionary
            subdict_str = _select_block(dict_str[pos:], '{', '}')
            value = _parse_dict_recursive(subdict_str)
            pos_tmp = pos + len(subdict_str)
        else:
            raise ValueError('error when parsing dict: unknown elem')

        key = key.strip('"')
        if len(key) > 0:
            dict_out[key] = value

        pos_last = dict_str.find(',', pos_tmp)
        if pos_last < 0:
            break
        pos_last += 1
        pos = dict_str.find(':', pos_last)

    return dict_out