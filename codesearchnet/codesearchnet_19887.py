def save(abf,fname=None,tag=None,width=700,close=True,facecolor='w',
              resize=True):
    """
    Save the pylab figure somewhere.
    If fname==False, show it instead.
    Height force > dpi force
    if a tag is given instead of a filename, save it alongside the ABF
    """
    if len(pylab.gca().get_lines())==0:
        print("can't save, no figure!")
        return
    if resize:
        pylab.tight_layout()
        pylab.subplots_adjust(bottom=.1)
    annotate(abf)
    if tag:
        fname = abf.outpath+abf.ID+"_"+tag+".png"
    inchesX,inchesY = pylab.gcf().get_size_inches()
    dpi=width/inchesX
    if fname:
        if not os.path.exists(abf.outpath):
            os.mkdir(abf.outpath)
        print(" <- saving [%s] at %d DPI (%dx%d)"%(os.path.basename(fname),dpi,inchesX*dpi,inchesY*dpi))
        pylab.savefig(fname,dpi=dpi,facecolor=facecolor)
    else:
        pylab.show()
    if close:
        pylab.close()