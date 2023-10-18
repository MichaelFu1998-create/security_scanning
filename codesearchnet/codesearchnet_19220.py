def ppdict(dict_to_print, br='\n', html=False, key_align='l', sort_keys=True,
           key_preffix='', key_suffix='', value_prefix='', value_suffix='', left_margin=3, indent=2):
    """Indent representation of a dict"""
    if dict_to_print:
        if sort_keys:
            dic = dict_to_print.copy()
            keys = list(dic.keys())
            keys.sort()
            dict_to_print = OrderedDict()
            for k in keys:
                dict_to_print[k] = dic[k]

        tmp = ['{']
        ks = [type(x) == str and "'%s'" % x or x for x in dict_to_print.keys()]
        vs = [type(x) == str and "'%s'" % x or x for x in dict_to_print.values()]
        max_key_len = max([len(str(x)) for x in ks])

        for i in range(len(ks)):
            k = {1: str(ks[i]).ljust(max_key_len),
                 key_align == 'r': str(ks[i]).rjust(max_key_len)}[1]

            v = vs[i]
            tmp.append(' ' * indent + '{}{}{}:{}{}{},'.format(key_preffix, k, key_suffix,
                                                              value_prefix, v, value_suffix))

        tmp[-1] = tmp[-1][:-1]  # remove the ',' in the last item
        tmp.append('}')

        if left_margin:
            tmp = [' ' * left_margin + x for x in tmp]

        if html:
            return '<code>{}</code>'.format(br.join(tmp).replace(' ', '&nbsp;'))
        else:
            return br.join(tmp)
    else:
        return '{}'