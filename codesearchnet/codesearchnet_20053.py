def genPNGs(folder,files=None):
    """Convert each TIF to PNG. Return filenames of new PNGs."""
    if files is None:
        files=glob.glob(folder+"/*.*")
    new=[]
    for fname in files:
        ext=os.path.basename(fname).split(".")[-1].lower()
        if ext in ['tif','tiff']:
            if not os.path.exists(fname+".png"):
                print(" -- converting %s to PNG..."%os.path.basename(fname))
                cm.image_convert(fname)
                new.append(fname) #fancy burn-in of image data
            else:
                pass
                #print(" -- already converted %s to PNG..."%os.path.basename(fname))
    return new