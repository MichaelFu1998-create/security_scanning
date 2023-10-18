def expMenu(groups,folder):
    """read experiment.txt and return a dict with [firstOfNewExp, color, star, comments]."""
    ### GENERATE THE MENU DATA BASED ON EXPERIMENT FILE
    orphans = sorted(list(groups.keys()))
    menu=[]
    if os.path.exists(folder+'/experiment.txt'):
        with open(folder+'/experiment.txt') as f:
            raw=f.read()
    else:
        raw=""
    for line in raw.split("\n"):
        item={}
        if len(line)==0:
            continue
        if line.startswith("~"):
            line=line[1:].split(" ",2)
            item["ID"]=line[0]
            item["symbol"]=''
            if len(line)>1:
                item["color"]=line[1]
            else:
                item["color"]="white"
            if len(line)>2 and len(line[2]):
                item["comment"]=line[2]
                if item["comment"][0]=="*":
                    item["symbol"]='*'
            else:
                item["comment"]=''
            if item["ID"] in orphans:
                orphans.remove(item["ID"])
        elif line.startswith("###"):
            line=line[3:].strip().split(" ",1)
            item["title"]=line[0]
            item["comment"]=''
            if len(line)>1:
                if line[1].startswith("- "):
                    line[1]=line[1][2:]
                item["comment"]=line[1]
        else:
            item["unknown"]=line
        menu.append(item)
    menu.append({"title":"orphans","comment":""})
    for ophan in orphans:
        menu.append({"orphan":ophan,"ID":ophan,"color":'',"symbol":'',"comment":''})
    return menu