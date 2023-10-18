def scanABFfolder(abfFolder):
    """
    scan an ABF directory and subdirectory. Try to do this just once.
    Returns ABF files, SWHLab files, and groups.
    """
    assert os.path.isdir(abfFolder)
    filesABF=forwardSlash(sorted(glob.glob(abfFolder+"/*.*")))
    filesSWH=[]
    if os.path.exists(abfFolder+"/swhlab4/"):
        filesSWH=forwardSlash(sorted(glob.glob(abfFolder+"/swhlab4/*.*")))
    groups=getABFgroups(filesABF)
    return filesABF,filesSWH,groups