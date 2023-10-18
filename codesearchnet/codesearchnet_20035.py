def filesByType(fileList):
    """
    given a list of files, return them as a dict sorted by type:
        * plot, tif, data, other
    """
    features=["plot","tif","data","other","experiment"]
    files={}
    for feature in features:
        files[feature]=[]
    for fname in fileList:
        other=True
        for feature in features:
            if "_"+feature+"_" in fname:
                files[feature].extend([fname])
                other=False
        if other:
            files['other'].extend([fname])
    return files