def add_icon(icon_data, dest):
    """
    Add icon to docset
    """
    with open(os.path.join(dest, "icon.png"), "wb") as f:
        f.write(icon_data)