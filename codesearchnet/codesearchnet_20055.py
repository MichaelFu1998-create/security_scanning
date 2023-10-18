def htmlABF(ID,group,d,folder,overwrite=False):
    """given an ID and the dict of files, generate a static html for that abf."""
    fname=folder+"/swhlab4/%s_index.html"%ID
    if overwrite is False and os.path.exists(fname):
        return
    html=TEMPLATES['abf']
    html=html.replace("~ID~",ID)
    html=html.replace("~CONTENT~",htmlABFcontent(ID,group,d))
    print(" <- writing [%s]"%os.path.basename(fname))
    with open(fname,'w') as f:
        f.write(html)
    return