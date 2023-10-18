def string_from_seconds(seconds):
    '''
    Converts seconds into elapsed time string of form 
    
    (X days(s)?,)? HH:MM:SS.YY
    
    '''
    td = str(timedelta(seconds = seconds))
    parts = td.split('.')
    if len(parts) == 1:
        td = td+'.00'
    elif len(parts) == 2:
        td = '.'.join([parts[0],parts[1][:2]])
    return td