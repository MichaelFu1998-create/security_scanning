def doStuff(ABFfolder,analyze=False,convert=False,index=True,overwrite=True,
            launch=True):
    """Inelegant for now, but lets you manually analyze every ABF in a folder."""
    IN=INDEX(ABFfolder)
    if analyze:
        IN.analyzeAll()
    if convert:
        IN.convertImages()