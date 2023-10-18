def getIDsFromFiles(files):
    """given a path or list of files, return ABF IDs."""
    if type(files) is str:
        files=glob.glob(files+"/*.*")
    IDs=[]
    for fname in files:
        if fname[-4:].lower()=='.abf':
            ext=fname.split('.')[-1]
            IDs.append(os.path.basename(fname).replace('.'+ext,''))
    return sorted(IDs)