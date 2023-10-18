def getIDfileDict(files):
    """
    given a list of files, return a dict[ID]=[files].
    This is made to assign children files to parent ABF IDs.
    """
    d={}
    orphans=[]
    for fname in files:
        if fname.endswith(".abf"):
            d[os.path.basename(fname)[:-4]]=[]
    for fname in files:
        if fname.endswith(".html") or fname.endswith(".txt"):
            continue #don't try to assign to an ABF
        if len(os.path.basename(fname).split(".")[0])>=8:
            ID = os.path.basename(fname)[:8] #ABF ID (first several chars)
        else:
            ID = os.path.basename(fname).split(".")[0] #short filename, just not extension
        if ID in d.keys():
            d[ID]=d[ID]+[fname]
        else:
            orphans.append(os.path.basename(fname))
            #print(" ?? orphan file",ID,os.path.basename(fname))
    if orphans:
        print(" ?? found %d orphan files"%len(orphans))
    return d