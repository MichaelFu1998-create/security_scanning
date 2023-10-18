def lazygo(watchFolder='../abfs/',reAnalyze=False,rebuildSite=False,
           keepGoing=True,matching=False):
    """
    continuously monitor a folder for new abfs and try to analyze them.
    This is intended to watch only one folder, but can run multiple copies.
    """
    abfsKnown=[]

    while True:
        print()
        pagesNeeded=[]
        for fname in glob.glob(watchFolder+"/*.abf"):
            ID=os.path.basename(fname).replace(".abf","")
            if not fname in abfsKnown:
                if os.path.exists(fname.replace(".abf",".rsv")): #TODO: or something like this
                    continue
                if matching and not matching in fname:
                    continue
                abfsKnown.append(fname)
                if os.path.exists(os.path.dirname(fname)+"/swhlab4/"+os.path.basename(fname).replace(".abf","_info.pkl")) and reAnalyze==False:
                    print("already analyzed",os.path.basename(fname))
                    if rebuildSite:
                        pagesNeeded.append(ID)
                else:
                    handleNewABF(fname)
                    pagesNeeded.append(ID)
        if len(pagesNeeded):
            print(" -- rebuilding index page")
            indexing.genIndex(os.path.dirname(fname),forceIDs=pagesNeeded)
        if not keepGoing:
            return
        for i in range(50):
            print('.',end='')
            time.sleep(.2)