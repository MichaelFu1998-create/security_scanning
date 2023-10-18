def filesByCell(fnames,cells):
    """given files and cells, return a dict of files grouped by cell."""
    byCell={}
    fnames=smartSort(fnames)
    days = list(set([elem[:5] for elem in fnames if elem.endswith(".abf")])) # so pythonic!
    for day in smartSort(days):
        parent=None
        for i,fname in enumerate([elem for elem in fnames if elem.startswith(day) and elem.endswith(".abf")]):
            ID=os.path.splitext(fname)[0]
            if len([x for x in fnames if x.startswith(ID)])-1:
                parent=ID
            if not parent in byCell:
                byCell[parent]=[]
            byCell[parent]=byCell[parent]+[fname]
    return byCell