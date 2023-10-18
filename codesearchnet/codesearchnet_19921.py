def findCells(fnames):
    """
    given a list of files, return a list of cells by their ID.
    A cell is indicated when an ABF name matches the start of another file.
    
    Example:
        123456.abf
        123456-whatever.tif 
    """
    IDs=[]
    filesByExt = filesByExtension(fnames)
    for abfFname in filesByExt['abf']:
        ID=os.path.splitext(abfFname)[0]
        for picFname in filesByExt['jpg']+filesByExt['tif']:
            if picFname.startswith(ID):
                IDs.append(ID)
                break
    return smartSort(IDs)