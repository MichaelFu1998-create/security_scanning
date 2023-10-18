def parse_byteranges(cls, environ):
        """
        Outputs a list of tuples with ranges or the empty list
        According to the rfc, start or end values can be omitted
        """
        r = []
        s = environ.get(cls.header_range, '').replace(' ','').lower()
        if s:
            l = s.split('=')
            if len(l) == 2:
                unit, vals = tuple(l)
                if unit == 'bytes' and vals:
                    gen_rng = ( tuple(rng.split('-')) for rng in vals.split(',') if '-' in rng )
                    for start, end in gen_rng:
                        if start or end:
                            r.append( (int(start) if start else None, int(end) if end else None) )
        return r