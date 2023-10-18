def _read_compound_from_factsage_file_(file_name):
    """
    Build a dictionary containing the factsage thermochemical data of a
    compound by reading the data from a file.

    :param file_name: Name of file to read the data from.

    :returns: Dictionary containing compound data.
    """

    with open(file_name) as f:
        lines = f.readlines()

    compound = {'Formula': lines[0].split(' ')[1]}
    # FIXME: replace with logging
    print(compound['Formula'])
    compound['Phases'] = phs = {}

    started = False
    phaseold = 'zz'
    recordold = '0'

    for line in lines:
        if started:
            if line.startswith('_'):  # line indicating end of data
                break
            line = line.replace(' 298 ', ' 298.15 ')
            line = line.replace(' - ', ' ')
            while '  ' in line:
                line = line.replace('  ', ' ')
            line = line.replace(' \n', '')
            line = line.replace('\n', '')
            strings = line.split(' ')
            if len(strings) < 2:  # empty line
                continue
            phase = strings[0]
            if phase != phaseold:  # new phase detected
                phaseold = phase
                ph = phs[phase] = {}
                ph['Symbol'] = phase
                ph['DHref'] = float(strings[2])
                ph['Sref'] = float(strings[3])
                cprecs = ph['Cp_records'] = {}
                record = strings[1]
                if record != recordold:  # new record detected
                    recordold = record
                    Tmax = float(strings[len(strings) - 1])
                    cprecs[Tmax] = {}
                    cprecs[Tmax]['Tmin'] = float(strings[len(strings) - 2])
                    cprecs[Tmax]['Tmax'] = float(strings[len(strings) - 1])
                    cprecs[Tmax]['Terms'] = []
                    t = {'Coefficient': float(strings[4]),
                         'Exponent': float(strings[5])}
                    cprecs[Tmax]['Terms'].append(t)
                    if len(strings) == 10:
                        t = {'Coefficient': float(strings[6]),
                             'Exponent': float(strings[7])}
                        cprecs[Tmax]['Terms'].append(t)
                else:  # old record detected
                    t = {'Coefficient': float(strings[2]),
                         'Exponent': float(strings[3])}
                    cprecs[Tmax]['Terms'].append(t)
                    if len(strings) == 8:
                        t = {'Coefficient': float(strings[4]),
                             'Exponent': float(strings[5])}
                        cprecs[Tmax]['Terms'].append(t)
            else:  # old phase detected
                ph = phs[phase]
                record = strings[1]
                if record != recordold:  # new record detected
                    recordold = record
                    Tmax = float(strings[len(strings) - 1])
                    cprecs = ph['Cp_records']
                    cprecs[Tmax] = {}
                    cprecs[Tmax]['Tmin'] = float(strings[len(strings) - 2])
                    cprecs[Tmax]['Tmax'] = float(strings[len(strings) - 1])
                    cprecs[Tmax]['Terms'] = []
                    t = {'Coefficient': float(strings[2]),
                         'Exponent': float(strings[3])}
                    cprecs[Tmax]['Terms'].append(t)
                    if len(strings) == 8:
                        t = {'Coefficient': float(strings[4]),
                             'Exponent': float(strings[5])}
                        cprecs[Tmax]['Terms'].append(t)
                else:  # old record detected
                    t = {'Coefficient': float(strings[2]),
                         'Exponent': float(strings[3])}
                    cprecs[Tmax]['Terms'].append(t)
                    if len(strings) == 8:
                        t = {'Coefficient': float(strings[4]),
                             'Exponent': float(strings[5])}
                        cprecs[Tmax]['Terms'].append(t)
        if line.startswith('_'):  # line indicating the start of the data
            started = True

    for name, ph in phs.items():
        cprecs = ph['Cp_records']
        first = cprecs[min(cprecs.keys())]
        first['Tmin'] = 298.15

    return compound