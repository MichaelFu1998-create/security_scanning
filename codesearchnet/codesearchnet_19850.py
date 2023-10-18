def getNotesForABF(abfFile):
    """given an ABF, find the parent, return that line of experiments.txt"""
    parent=getParent(abfFile)
    parent=os.path.basename(parent).replace(".abf","")
    expFile=os.path.dirname(abfFile)+"/experiment.txt"
    if not os.path.exists(expFile):
        return "no experiment file"
    with open(expFile) as f:
        raw=f.readlines()
    for line in raw:
        if line[0]=='~':
            line=line[1:].strip()
            if line.startswith(parent):
                while "\t\t" in line:
                    line=line.replace("\t\t","\t")
                line=line.replace("\t","\n")
                return line
    return "experiment.txt found, but didn't contain %s"%parent