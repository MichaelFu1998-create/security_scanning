def checkOut(thing,html=True):
    """show everything we can about an object's projects and methods."""
    msg=""
    for name in sorted(dir(thing)):
        if not "__" in name:
            msg+="<b>%s</b>\n"%name
            try:
                msg+=" ^-VALUE: %s\n"%getattr(thing,name)()
            except:
                pass
    if html:
        html='<html><body><code>'+msg+'</code></body></html>'
        html=html.replace(" ","&nbsp;").replace("\n","<br>")
        fname = tempfile.gettempdir()+"/swhlab/checkout.html"
        with open(fname,'w') as f:
            f.write(html)
        webbrowser.open(fname)
    print(msg.replace('<b>','').replace('</b>',''))