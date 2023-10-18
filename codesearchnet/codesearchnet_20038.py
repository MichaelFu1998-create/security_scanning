def abfFname_Save(abfFname):
    """return the path of the last loaded ABF."""
    fname=userFolder()+"/abfFname.ini"
    with open(fname,'w') as f:
        f.write(os.path.abspath(abfFname))
    return