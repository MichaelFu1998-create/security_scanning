def _strOrDate(st):
    '''internal'''
    if isinstance(st, string_types):
        return st
    elif isinstance(st, datetime):
        return st.strftime('%Y%m%d')
    raise PyEXception('Not a date: %s', str(st))