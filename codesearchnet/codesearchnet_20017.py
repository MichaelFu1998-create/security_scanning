def analyzeSingle(abfFname):
    """Reanalyze data for a single ABF. Also remakes child and parent html."""
    assert os.path.exists(abfFname) and abfFname.endswith(".abf")
    ABFfolder,ABFfname=os.path.split(abfFname)
    abfID=os.path.splitext(ABFfname)[0]
    IN=INDEX(ABFfolder)
    IN.analyzeABF(abfID)
    IN.scan()
    IN.html_single_basic([abfID],overwrite=True)
    IN.html_single_plot([abfID],overwrite=True)
    IN.scan()
    IN.html_index()

    return