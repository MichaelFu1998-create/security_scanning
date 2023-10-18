def waitTillCopied(fname):
    """
    sometimes a huge file takes several seconds to copy over.
    This will hang until the file is copied (file size is stable).
    """
    lastSize=0
    while True:
        thisSize=os.path.getsize(fname)
        print("size:",thisSize)
        if lastSize==thisSize:
            print("size: STABLE")
            return
        else:
            lastSize=thisSize
        time.sleep(.1)