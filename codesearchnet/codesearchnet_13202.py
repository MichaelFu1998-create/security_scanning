def import_lab(namespace, filename, infer_duration=True, **parse_options):
    r'''Load a .lab file as an Annotation object.

    .lab files are assumed to have the following format:

        ``TIME_START\tTIME_END\tANNOTATION``

    By default, .lab files are assumed to have columns separated by one
    or more white-space characters, and have no header or index column
    information.

    If the .lab file contains only two columns, then an empty duration
    field is inferred.

    If the .lab file contains more than three columns, each row's
    annotation value is assigned the contents of last non-empty column.


    Parameters
    ----------
    namespace : str
        The namespace for the new annotation

    filename : str
        Path to the .lab file

    infer_duration : bool
        If `True`, interval durations are inferred from `(start, end)` columns,
        or difference between successive times.

        If `False`, interval durations are assumed to be explicitly coded as
        `(start, duration)` columns.  If only one time column is given, then
        durations are set to 0.

        For instantaneous event annotations (e.g., beats or onsets), this
        should be set to `False`.

    parse_options : additional keyword arguments
        Passed to ``pandas.DataFrame.read_csv``

    Returns
    -------
    annotation : Annotation
        The newly constructed annotation object

    See Also
    --------
    pandas.DataFrame.read_csv
    '''

    # Create a new annotation object
    annotation = core.Annotation(namespace)

    parse_options.setdefault('sep', r'\s+')
    parse_options.setdefault('engine', 'python')
    parse_options.setdefault('header', None)
    parse_options.setdefault('index_col', False)

    # This is a hack to handle potentially ragged .lab data
    parse_options.setdefault('names', range(20))

    data = pd.read_csv(filename, **parse_options)

    # Drop all-nan columns
    data = data.dropna(how='all', axis=1)

    # Do we need to add a duration column?
    # This only applies to event annotations
    if len(data.columns) == 2:
        # Insert a column of zeros after the timing
        data.insert(1, 'duration', 0)
        if infer_duration:
            data['duration'][:-1] = data.loc[:, 0].diff()[1:].values

    else:
        # Convert from time to duration
        if infer_duration:
            data.loc[:, 1] -= data[0]

    for row in data.itertuples():
        time, duration = row[1:3]

        value = [x for x in row[3:] if x is not None][-1]

        annotation.append(time=time,
                          duration=duration,
                          confidence=1.0,
                          value=value)

    return annotation