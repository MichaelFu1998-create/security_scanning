def _toDatetime(df, cols=None, tcols=None):
    '''internal'''
    cols = cols or _STANDARD_DATE_FIELDS
    tcols = tcols = _STANDARD_TIME_FIELDS

    for col in cols:
        if col in df:
            df[col] = pd.to_datetime(df[col], infer_datetime_format=True, errors='coerce')

    for tcol in tcols:
        if tcol in df:
            df[tcol] = pd.to_datetime(df[tcol], unit='ms', errors='coerce')