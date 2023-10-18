def getABFgroups(files):
    """
    given a list of ALL files (not just ABFs), return a dict[ID]=[ID,ID,ID].
    Parents are determined if a .abf matches a .TIF.
    This is made to assign children files to parent ABF IDs.
    """
    children=[]
    groups={}
    for fname in sorted(files):
        if fname.endswith(".abf"):
            if fname.replace(".abf",".TIF") in files: #TODO: cap sensitive
                if len(children):
                    groups[children[0]]=children
                children=[os.path.basename(fname)[:-4]]
            else:
                children.append(os.path.basename(fname)[:-4])
    groups[children[0]]=children
    #print(" -- found %d groups of %d ABFs"%(len(groups),len(files)))
    return groups