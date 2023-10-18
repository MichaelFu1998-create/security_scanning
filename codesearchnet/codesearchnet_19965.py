def fileModifiedTimestamp(fname):
    """return "YYYY-MM-DD" when the file was modified."""
    modifiedTime=os.path.getmtime(fname)
    stamp=time.strftime('%Y-%m-%d', time.localtime(modifiedTime))
    return stamp