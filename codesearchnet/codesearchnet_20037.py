def abfFname_Load():
    """return the path of the last loaded ABF."""
    fname=userFolder()+"/abfFname.ini"
    if os.path.exists(fname):
        abfFname=open(fname).read().strip()
        if os.path.exists(abfFname) or abfFname.endswith("_._"):
            return abfFname
    return os.path.abspath(os.sep)