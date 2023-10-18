def abfGroups(abfFolder):
    """
    Given a folder path or list of files, return groups (dict) by cell.

    Rules which define parents (cells):
        * assume each cell has one or several ABFs
        * that cell can be labeled by its "ID" or "parent" ABF (first abf)
        * the ID is just the filename of the first abf without .abf
        * if any file starts with an "ID", that ID becomes a parent.
        * examples could be 16o14044.TIF or 16o14044-cell1-stuff.jpg
        * usually this is done by saving a pic of the cell with same filename

    Returns a dict of "parent IDs" representing the "children"
        groups["16o14041"] = ["16o14041","16o14042","16o14043"]

    From there, getting children files is trivial. Just find all files in
    the same folder whose filenames begin with one of the children.
    """

    # prepare the list of files, filenames, and IDs
    files=False
    if type(abfFolder) is str and os.path.isdir(abfFolder):
        files=abfSort(os.listdir(abfFolder))
    elif type(abfFolder) is list:
        files=abfSort(abfFolder)
    assert type(files) is list
    files=list_to_lowercase(files)

    # group every filename in a different list, and determine parents
    abfs, IDs, others, parents, days = [],[],[],[],[]
    for fname in files:
        if fname.endswith(".abf"):
            abfs.append(fname)
            IDs.append(fname[:-4])
            days.append(fname[:5])
        else:
            others.append(fname)
    for ID in IDs:
        for fname in others:
            if fname.startswith(ID):
                parents.append(ID)
    parents=abfSort(set(parents)) # allow only one copy each
    days=abfSort(set(days)) # allow only one copy each

    # match up children with parents, respecting daily orphans.
    groups={}
    for day in days:
        parent=None
        for fname in [x for x in abfs if x.startswith(day)]:
            ID=fname[:-4]
            if ID in parents:
                parent=ID
            if not parent in groups.keys():
                groups[parent]=[]
            groups[parent].extend([ID])
    return groups