def loadResults(resultsFile):
    """returns a dict of active folders with days as keys."""
    with open(resultsFile) as f:
        raw=f.read().split("\n")
    foldersByDay={}
    for line in raw:
        folder=line.split('"')[1]+"\\"
        line=[]+line.split('"')[2].split(", ")
        for day in line[1:]:
            if not day in foldersByDay:
                foldersByDay[day]=[]
            foldersByDay[day]=foldersByDay[day]+[folder]
    nActiveDays=len(foldersByDay)
    dayFirst=sorted(foldersByDay.keys())[0]
    dayLast=sorted(foldersByDay.keys())[-1]
    dayFirst=datetime.datetime.strptime(dayFirst, "%Y-%m-%d" )
    dayLast=datetime.datetime.strptime(dayLast, "%Y-%m-%d" )
    nDays = (dayLast - dayFirst).days + 1
    emptyDays=0
    for deltaDays in range(nDays):
        day=dayFirst+datetime.timedelta(days=deltaDays)
        stamp=datetime.datetime.strftime(day, "%Y-%m-%d" )
        if not stamp in foldersByDay:
            foldersByDay[stamp]=[]
            emptyDays+=1
    percActive=nActiveDays/nDays*100
    print("%d of %d days were active (%.02f%%)"%(nActiveDays,nDays,percActive))
    return foldersByDay