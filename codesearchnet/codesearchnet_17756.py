def ld_to_dl(ld):
    '''
    Convert list of dictionaries to dictionary of lists
    '''
    if ld:
        keys = list(ld[0])
        dl = {key:[d[key] for d in ld] for key in keys}
        return dl
    else:
        return {}