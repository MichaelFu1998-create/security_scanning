def filesByExtension(fnames):
    """given a list of files, return a dict organized by extension."""
    byExt={"abf":[],"jpg":[],"tif":[]} # prime it with empties
    for fname in fnames:
        ext = os.path.splitext(fname)[1].replace(".",'').lower()
        if not ext in byExt.keys():
            byExt[ext]=[]
        byExt[ext]=byExt[ext]+[fname]
    return byExt