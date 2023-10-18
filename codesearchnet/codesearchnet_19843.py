def groupsFromKey(keyFile='./key.txt'):
    """
    given a groups file, return a dict of groups.
    Example:
        ### GROUP: TR
        16602083
        16608059
        ### GROUP: TU
        16504000
        16507011
    """
    groups={}
    thisGroup="?"
    with open(keyFile) as f:
        raw=f.read().split("\n")
    for line in raw:
        line=line.strip()
        if len(line)<3:
            continue
        if "### GROUP" in line:
            thisGroup=line.split(": ")[1]
            groups[thisGroup]=[]
        else:
            groups[thisGroup]=groups[thisGroup]+[line]
    return groups