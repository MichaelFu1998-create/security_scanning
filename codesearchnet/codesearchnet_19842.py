def msgDict(d,matching=None,sep1="=",sep2="\n",sort=True,cantEndWith=None):
    """convert a dictionary to a pretty formatted string."""
    msg=""
    if "record" in str(type(d)):
        keys=d.dtype.names
    else:
        keys=d.keys()
    if sort:
        keys=sorted(keys)
    for key in keys:
        if key[0]=="_":
            continue
        if matching:
            if not key in matching:
                continue
        if cantEndWith and key[-len(cantEndWith)]==cantEndWith:
            continue
        if 'float' in str(type(d[key])):
            s="%.02f"%d[key]
        else:
            s=str(d[key])
        if "object" in s:
            s='<object>'
        msg+=key+sep1+s+sep2
    return msg.strip()