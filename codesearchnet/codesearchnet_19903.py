def processFolder(abfFolder):
    """call processAbf() for every ABF in a folder."""
    if not type(abfFolder) is str or not len(abfFolder)>3:
        return
    files=sorted(glob.glob(abfFolder+"/*.abf"))
    for i,fname in enumerate(files):
        print("\n\n\n### PROCESSING {} of {}:".format(i,len(files)),os.path.basename(fname))
        processAbf(fname,show=False)
    plt.show()
    return