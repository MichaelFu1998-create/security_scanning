def indexImages(folder,fname="index.html"):
    """OBSOLETE WAY TO INDEX A FOLDER.""" #TODO: REMOVE
    html="<html><body>"
    for item in glob.glob(folder+"/*.*"):
        if item.split(".")[-1] in ['jpg','png']:
            html+="<h3>%s</h3>"%os.path.basename(item)
            html+='<img src="%s">'%os.path.basename(item)
            html+='<br>'*10
    html+="</html></body>"
    f=open(folder+"/"+fname,'w')
    f.write(html)
    f.close
    print("indexed:")
    print("  ",os.path.abspath(folder+"/"+fname))
    return