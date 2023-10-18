def downloadURL(url, filename):
    """
        Inconditianilly download the URL in a temporary directory.
        When finished, the file is moved in the real directory.
        Like this an other process will not attempt to extract an inclomplete file.
    """
    path_temp_bviewfile = os.path.join(c.raw_data, c.bview_dir, 'tmp', filename)
    path_bviewfile = os.path.join(c.raw_data, c.bview_dir, filename)
    try:
        f = urlopen(url)
    except:
        return False
    if f.getcode() != 200:
        publisher.warning('{} unavailable, code: {}'.format(url, f.getcode()))
        return False
    try:
        with open(path_temp_bviewfile, 'w') as outfile:
            outfile.write(f.read())
        os.rename(path_temp_bviewfile, path_bviewfile)
    except:
        os.remove(path_temp_bviewfile)
        return False
    return True