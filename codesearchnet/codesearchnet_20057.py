def genIndex(folder,forceIDs=[]):
    """expects a folder of ABFs."""
    if not os.path.exists(folder+"/swhlab4/"):
        print(" !! cannot index if no /swhlab4/")
        return
    timestart=cm.timethis()
    files=glob.glob(folder+"/*.*") #ABF folder
    files.extend(glob.glob(folder+"/swhlab4/*.*"))
    print(" -- indexing glob took %.02f ms"%(cm.timethis(timestart)*1000))
    files.extend(genPNGs(folder,files))
    files=sorted(files)
    timestart=cm.timethis()
    d=cm.getIDfileDict(files) #TODO: this is really slow
    print(" -- filedict length:",len(d))
    print(" -- generating ID dict took %.02f ms"%(cm.timethis(timestart)*1000))
    groups=cm.getABFgroups(files)
    print(" -- groups length:",len(groups))
    for ID in sorted(list(groups.keys())):
        overwrite=False
        for abfID in groups[ID]:
            if abfID in forceIDs:
                overwrite=True
        try:
            htmlABF(ID,groups[ID],d,folder,overwrite)
        except:
            print("~~ HTML GENERATION FAILED!!!")
    menu=expMenu(groups,folder)
    makeSplash(menu,folder)
    makeMenu(menu,folder)
    htmlFrames(d,folder)
    makeMenu(menu,folder)
    makeSplash(menu,folder)