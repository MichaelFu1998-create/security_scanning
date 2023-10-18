def TIF_to_jpg_all(path):
    """run TIF_to_jpg() on every TIF of a folder."""
    for fname in sorted(glob.glob(path+"/*.tif")):
        print(fname)
        TIF_to_jpg(fname)