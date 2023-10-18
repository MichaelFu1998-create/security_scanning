def HTML_results(resultsFile):
    """generates HTML report of active folders/days."""
    foldersByDay=loadResults(resultsFile)

    # optionally skip dates before a certain date
#    for day in sorted(list(foldersByDay.keys())):
#        if time.strptime(day,"%Y-%m-%d")<time.strptime("2016-05-01","%Y-%m-%d"):
#            del foldersByDay[day]

    # Create a header
    html="<div class='heading'>Active Folder Report (updated TIMESTAMP)</div>"
    html+="<li>When a file is created (or modified) its parent folder is marked active for that day."
    html+="<li>This page reports all folders which were active in the last several years. "
    html+="<li>A single folder can be active for more than one date."
    html=html.replace("TIMESTAMP",(time.strftime('%Y-%m-%d', time.localtime())))
    html+="<br>"*5


    # create menu at the top of the page
    html+="<div class='heading'>Active Folder Dates</div>"
    html+="<code>"
    lastMonth=""
    lastYear=""
    for day in sorted(list(foldersByDay.keys())):
        month=day[:7]
        year=day[:4]
        if year!=lastYear:
            html+="<br><br><b style='font-size: 200%%;'>%s</b> "%year
            lastYear=year
        if month!=lastMonth:
            html+="<br><b>%s:</b> "%month
            lastMonth=month
        html+="<a href='#%s'>%s</a>, "%(day,day[8:])
    html+="<br>"*5
    html=html.replace(", <br>","<br>")
    html+="</code>"

    # create the full list of folders organized by active date
    html+="<div class='heading'>Active Folders</div>"
    for day in sorted(list(foldersByDay.keys())):
        dt=datetime.datetime.strptime(day, "%Y-%m-%d" )
        classPrefix="weekday"
        if int(dt.weekday())>4:
            classPrefix="weekend"
        html+="<a name='%s' href='#%s' style='color: black;'>"%(day,day)
        title="%s (%s)"%(day,DAYSOFWEEK[dt.weekday()])
        html+="<div class='%s_datecode'>%s</div></a>"%(classPrefix,title)
        html+="<div class='%s_folders'>"%(classPrefix)
        # define folders to skip
        for folder in foldersByDay[day]:
            if "\\References\\" in folder:
                continue
            if "\\MIP\\" in folder:
                continue
            if "LineScan-" and "\\analysis\\" in folder:
                continue
            if "trakem2" in folder:
                continue
            if "SWHlab-" in folder:
                continue
            if "\\swhlab" in folder:
                continue
            html+="%s<br>"%folder
        html+="</div>"
    fnameSave=resultsFile+".html"
    html=html.replace("D:\\X_Drive\\","X:\\")
    with open(fnameSave,'w') as f:
        f.write(HTML_TEMPLATE.replace("<body>","<body>"+html))
    print("saved",fnameSave)