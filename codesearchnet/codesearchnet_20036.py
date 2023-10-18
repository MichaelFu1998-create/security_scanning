def userFolder():
    """return the semi-temporary user folder"""
    #path=os.path.abspath(tempfile.gettempdir()+"/swhlab/")
    #don't use tempdir! it will get deleted easily.
    path=os.path.expanduser("~")+"/.swhlab/" # works on windows or linux
    # for me, path=r"C:\Users\swharden\.swhlab"
    if not os.path.exists(path):
        print("creating",path)
        os.mkdir(path)
    return os.path.abspath(path)