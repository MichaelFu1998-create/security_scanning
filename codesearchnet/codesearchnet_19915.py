def frames(fname=None,menuWidth=200,launch=False):
    """create and save a two column frames HTML file."""
    html="""
    <frameset cols="%dpx,*%%">
    <frame name="menu" src="index_menu.html">
    <frame name="content" src="index_splash.html">
    </frameset>"""%(menuWidth)
    with open(fname,'w') as f:
        f.write(html)
    if launch:
        webbrowser.open(fname)