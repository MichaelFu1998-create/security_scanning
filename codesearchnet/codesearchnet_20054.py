def htmlABFcontent(ID,group,d):
    """generate text to go inside <body> for single ABF page."""
    html=""
    files=[]
    for abfID in group:
        files.extend(d[abfID])
    files=sorted(files)

    #start with root images
    html+="<hr>"
    for fname in files:
        if ".png" in fname.lower() and not "swhlab4" in fname:
            fname="../"+os.path.basename(fname)
            html+='<a href="%s"><img src="%s" width="348"></a> '%(fname,fname)

    #progress to /swhlab4/ images
    html+="<hr>"
    #ABFinfo
    lastID=''
    for fname in sorted(files):
        if not "swhlab4" in fname:
            continue
        ID=os.path.basename(fname).split("_")[0]
        if not ID==lastID:
            lastID=ID
            html+="<h3>%s</h3>"%os.path.basename(fname).split("_")[0]
        if ".png" in fname.lower():
            fname=os.path.basename(fname)
            html+='<a href="%s"><img src="%s" height="300"></a> '%(fname,fname)
            continue

    html+="<hr>"
    for fname in files:
        if not "swhlab4" in fname:
            continue
        if ".pkl" in fname:
            callit=os.path.basename(fname)
            thing=cm.getPkl(fname)
            if "_APs.pkl" in fname:
                callit+=" (first AP)"
                thing=cm.dictFlat(thing)
                if len(thing):
                    thing=thing[0]
            elif "_MTs.pkl" in fname:
                if type(thing) == dict:
                    callit+=" (from AVG of all sweeps)"
                else:
                    callit+=" (first sweep)"
                    thing=thing[0]
            elif "_SAP.pkl" in fname:
                continue #don't plot those, too complicated
            elif "_info.pkl" in fname or "_iv.pkl" in fname:
                pass #no trouble, go for it
            else:
                print(" ?? not sure how to index [%s]"%os.path.basename(fname))
                continue
            if type(thing) is dict:
                thing=cm.msgDict(thing)
            if type(thing) is list:
                out=''
                for item in thing:
                    out+=str(item)+"\n"
                thing=out
            thing=str(thing) #lol stringthing
            thing="### %s ###\n"%os.path.basename(fname)+thing

            # putting it in a textbox is obnoxious. put it in the source instead.
            #html+='<br><br><textarea rows="%d" cols="70">%s</textarea>'%(str(thing).count("\n")+5,thing)

            html+="(view source for %s) <!--\n\n%s\n\n-->"%(os.path.basename(fname),thing)

    return html