def readLog(fname="workdays.csv",onlyAfter=datetime.datetime(year=2017,month=1,day=1)):
    """return a list of [stamp, project] elements."""
    with open(fname) as f:
        raw=f.read().split("\n")
    efforts=[] #date,nickname
    for line in raw[1:]:
        line=line.strip().split(",")
        date=datetime.datetime.strptime(line[0], "%Y-%m-%d")
        if onlyAfter and date<onlyAfter:
            continue
        if len(line)<3:
            continue
        for project in line[2:]:
            project=project.strip()
            if len(project):
                efforts.append([date,project])
    return efforts