def getParent(abfFname):
    """given an ABF file name, return the ABF of its parent."""
    child=os.path.abspath(abfFname)
    files=sorted(glob.glob(os.path.dirname(child)+"/*.*"))
    parentID=abfFname #its own parent
    for fname in files:
        if fname.endswith(".abf") and fname.replace(".abf",".TIF") in files:
            parentID=os.path.basename(fname).replace(".abf","")
        if os.path.basename(child) in fname:
            break
    return parentID