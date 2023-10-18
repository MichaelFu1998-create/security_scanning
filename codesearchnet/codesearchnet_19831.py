def matrixToHTML(data,names=None,units=None,bookName=None,sheetName=None,xCol=None):
    """Put 2d numpy data into a temporary HTML file."""
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

    htmlFname = tempfile.gettempdir()+"/swhlab/WKS-%s.%s.html"%(bookName,sheetName)
    html="""<body>
    <style>
    body {
          background-color: #ababab;
          padding:20px;
          }
    table {
           font-size:12px;
           border-spacing: 0;
           border-collapse: collapse;
           //border:2px solid #000000;
           }
    .name {background-color:#fafac8;text-align:center;}
    .units {background-color:#fafac8;text-align:center;}
    .data0 {background-color:#FFFFFF;font-family: monospace;text-align:center;}
    .data1 {background-color:#FAFAFA;font-family: monospace;text-align:center;}
    .labelRow {background-color:#e0dfe4; text-align:right;border:1px solid #000000;}
    .labelCol {background-color:#e0dfe4; text-align:center;border:1px solid #000000;}
    td {
        border:1px solid #c0c0c0; padding:5px;
        //font-family: Verdana, Geneva, sans-serif;
        font-family: Arial, Helvetica, sans-serif
        }
    </style>
    <html>"""
    html+="<h1>FauxRigin</h1>"
    if bookName or sheetName:
        html+='<code><b>%s / %s</b></code><br><br>'%(bookName,sheetName)
    html+="<table>"
    #cols=list(range(len(names)))
    colNames=['']
    for i in range(len(units)):
        label="%s (%d)"%(chr(i+ord('A')),i)
        colNames.append(label)
    html+=htmlListToTR(colNames,'labelCol','labelCol')
    html+=htmlListToTR(['Long Name']+list(names),'name',td1Class='labelRow')
    html+=htmlListToTR(['Units']+list(units),'units',td1Class='labelRow')
    cutOff=False
    for y in range(len(data)):
        html+=htmlListToTR([y+1]+list(data[y]),trClass='data%d'%(y%2),td1Class='labelRow')
        if y>=200:
            cutOff=True
            break
    html+="</table>"
    html=html.replace(">nan<",">--<")
    html=html.replace(">None<","><")
    if cutOff:
        html+="<h3>... showing only %d of %d rows ...</h3>"%(y,len(data))
    html+="</body></html>"
    with open(htmlFname,'w') as f:
        f.write(html)
    webbrowser.open(htmlFname)
    return