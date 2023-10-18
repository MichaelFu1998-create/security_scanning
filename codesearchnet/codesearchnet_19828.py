def html_temp_launch(html):
    """given text, make it a temporary HTML file and launch it."""
    fname = tempfile.gettempdir()+"/swhlab/temp.html"
    with open(fname,'w') as f:
        f.write(html)
    webbrowser.open(fname)