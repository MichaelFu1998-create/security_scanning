def matrixToWks(data,names=None,units=None,bookName=None,sheetName=" ",xCol=None):
    """
    Put 2d numpy data into an Origin worksheet.
    If bookname and sheetname are given try to load data into that book/sheet.
    If the book/sheet doesn't exist, create it.
    """
    if type(data) is list:
        data=matrixfromDicts(data)
    if not names:
        names=[""]*len(data[0])
        if data.dtype.names:
            names=list(data.dtype.names)
    if not units:
        units=[""]*len(data[0])
        for i in range(len(units)):
            if names[i] in UNITS.keys():
                units[i]=UNITS[names[i]]
    if 'recarray' in str(type(data)): #make it a regular array
        data=data.view(float).reshape(data.shape + (-1,))
    if xCol and xCol in names:
        xCol=names.index(xCol)
        names.insert(0,names[xCol])
        units.insert(0,units[xCol])
        data=np.insert(data,0,data[:,xCol],1)

    if not bookName:
        bookName="tempBook"
    if not sheetName:
        sheetName="temp-"+str(time.clock())[-5:]

    try:
        import PyOrigin
        PyOrigin.LT_execute("") #try to crash a non-orign environment
    except:
        print(" -- PyOrigin not running, making HTML output.")
        matrixToHTML(data,names,units,bookName,sheetName,xCol)
        return

    nrows,ncols=len(data),len(data[0])
    if 'recarray' in str(type(data)): #convert structured array to regular array
        data=np.array(data.view(),dtype=float).reshape((nrows,ncols))
    data=np.transpose(data) #transpose it

    PyOrigin.LT_execute("activateSheet(%s, %s)"%(bookName,sheetName))
    wks=PyOrigin.ActiveLayer()
    while wks.GetColCount() < ncols:
        wks.InsertCol(wks.GetColCount(),'')
    for i in range(ncols):
        col=wks.Columns(i)
        col.SetLongName(names[i])
        col.SetUnits(units[i])
    wks.SetData(data,0,0)
    PyOrigin.LT_execute("FixNanBug")
    PyOrigin.LT_execute("ABFPathToMetaData")