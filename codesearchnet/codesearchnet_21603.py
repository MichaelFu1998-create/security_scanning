def dictify_urn(urn, combine_interval=True):
    """
        By default, this will put the `interval` as part of the `cell_methods`
        attribute (NetCDF CF style). To return `interval` as its own key, use
        the `combine_interval=False` parameter.
    """
    ioos_urn = IoosUrn.from_string(urn)

    if ioos_urn.valid() is False:
        return dict()

    if ioos_urn.asset_type != 'sensor':
        logger.error("This function only works on 'sensor' URNs.")
        return dict()

    if '#' in ioos_urn.component:
        standard_name, extras = ioos_urn.component.split('#')
    else:
        standard_name = ioos_urn.component
        extras = ''

    d = dict(standard_name=standard_name)

    # Discriminant
    if '-' in ioos_urn.component:
        d['discriminant'] = standard_name.split('-')[-1]
        d['standard_name'] = standard_name.split('-')[0]

    intervals = []
    cell_methods = []
    if extras:
        for section in extras.split(';'):
            key, values = section.split('=')
            if key == 'interval':
                # special case, intervals should be appended to the cell_methods
                for v in values.split(','):
                    intervals.append(v)
            else:
                if key == 'cell_methods':
                    value = [ x.replace('_', ' ').replace(':', ': ') for x in values.split(',') ]
                    cell_methods = value
                else:
                    value = ' '.join([x.replace('_', ' ').replace(':', ': ') for x in values.split(',')])
                    d[key] = value

    if combine_interval is True:
        if cell_methods and intervals:
            if len(cell_methods) == len(intervals):
                d['cell_methods'] = ' '.join([ '{} (interval: {})'.format(x[0], x[1].upper()) for x in zip(cell_methods, intervals) ])
            else:
                d['cell_methods'] = ' '.join(cell_methods)
                for i in intervals:
                    d['cell_methods'] += ' (interval: {})'.format(i.upper())
        elif cell_methods:
            d['cell_methods'] = ' '.join(cell_methods)
            for i in intervals:
                d['cell_methods'] += ' (interval: {})'.format(i.upper())
        elif intervals:
            raise ValueError("An interval without a cell_method is not allowed!  Not possible!")
    else:
        d['cell_methods'] = ' '.join(cell_methods)
        d['interval'] = ','.join(intervals).upper()

    if 'vertical_datum' in d:
        d['vertical_datum'] = d['vertical_datum'].upper()

    return d