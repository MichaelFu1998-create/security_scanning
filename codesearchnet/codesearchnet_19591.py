def walkfolder(toppath, pred):
    """
    walk folder if pred(foldername) is True
    :type toppath: str
    :type pred: function(str) => bool
    """
    for entry in scandir.scandir(toppath):
        if not entry.is_dir() or not pred(entry.name):
            continue
        yield entry.path
        for p in walkfolder(entry.path, pred):
            yield p