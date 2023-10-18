def save(html,fname=None,launch=False):
    """wrap HTML in a top and bottom (with css) and save to disk."""
    html=html_top+html+html_bot
    html=html.replace("~GENAT~",swhlab.common.datetimeToString())
    if fname is None:
        fname = tempfile.gettempdir()+"/temp.html"
        launch=True
    fname=os.path.abspath(fname)
    with open(fname,'w') as f:
        f.write(html)

    global stylesheetSaved
    stylesheetPath=os.path.join(os.path.dirname(fname),"style.css")
    if not os.path.exists(stylesheetPath) or stylesheetSaved is False:
        with open(stylesheetPath,'w') as f:
            f.write(stylesheet)
            stylesheetSaved=True
    if launch:
        webbrowser.open(fname)