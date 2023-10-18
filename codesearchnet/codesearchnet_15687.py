def amz_cano_querystring(qs):
        """
        Parse and format querystring as per AWS4 auth requirements.

        Perform percent quoting as needed.

        qs -- querystring

        """
        safe_qs_amz_chars = '&=+'
        safe_qs_unresvd = '-_.~'
        # If Python 2, switch to working entirely in str
        # as quote() has problems with Unicode
        if PY2:
            qs = qs.encode('utf-8')
            safe_qs_amz_chars = safe_qs_amz_chars.encode()
            safe_qs_unresvd = safe_qs_unresvd.encode()
        qs = unquote(qs)
        space = b' ' if PY2 else ' '
        qs = qs.split(space)[0]
        qs = quote(qs, safe=safe_qs_amz_chars)
        qs_items = {}
        for name, vals in parse_qs(qs, keep_blank_values=True).items():
            name = quote(name, safe=safe_qs_unresvd)
            vals = [quote(val, safe=safe_qs_unresvd) for val in vals]
            qs_items[name] = vals
        qs_strings = []
        for name, vals in qs_items.items():
            for val in vals:
                qs_strings.append('='.join([name, val]))
        qs = '&'.join(sorted(qs_strings))
        if PY2:
            qs = unicode(qs)
        return qs