def processAbf(abfFname,saveAs=False,dpi=100,show=True):
    """
    automatically generate a single representative image for an ABF.
    If saveAs is given (full path of a jpg of png file), the image will be saved.
    Otherwise, the image will pop up in a matplotlib window.
    """
    if not type(abfFname) is str or not len(abfFname)>3:
        return
    abf=swhlab.ABF(abfFname)
    plot=swhlab.plotting.ABFplot(abf)
    plot.figure_height=6
    plot.figure_width=10
    plot.subplot=False
    plot.figure(True)
    if abf.get_protocol_sequence(0)==abf.get_protocol_sequence(1) or abf.sweeps<2:
        # same protocol every time
        if abf.lengthMinutes<2:
            # short (probably a memtest or tau)
            ax1=plt.subplot(211)
            plot.figure_sweeps()
            plt.title("{} ({} sweeps)".format(abf.ID,abf.sweeps))
            plt.gca().get_xaxis().set_visible(False)
            plt.subplot(212,sharex=ax1)
            plot.figure_protocol()
            plt.title("")
        else:
            # long (probably a drug experiment)
            plot.figure_chronological()
    else:
        # protocol changes every sweep
        plots=[211,212] # assume we want 2 images
        if abf.units=='mV': # maybe it's something with APs?
            ap=swhlab.AP(abf) # go ahead and do AP detection
            ap.detect() # try to detect APs
            if len(ap.APs): # if we found some
                plots=[221,223,222,224] # get ready for 4 images
        ax1=plt.subplot(plots[0])
        plot.figure_sweeps()
        plt.title("{} ({} sweeps)".format(abf.ID,abf.sweeps))
        plt.gca().get_xaxis().set_visible(False)
        plt.subplot(plots[1],sharex=ax1)
        plot.figure_protocols()
        plt.title("protocol")
        if len(plots)>2:
            # assume we want to look at the first AP
            ax2=plt.subplot(plots[2])
            plot.rainbow=False
            plot.kwargs["color"]='b'
            plot.figure_chronological()
            plt.gca().get_xaxis().set_visible(False)
            plt.title("first AP magnitude")
            # velocity plot
            plt.subplot(plots[3],sharex=ax2)
            plot.abf.derivative=True
            plot.rainbow=False
            plot.traceColor='r'
            plot.figure_chronological()
            plt.axis([ap.APs[0]["T"]-.05,ap.APs[0]["T"]+.05,None,None])
            plt.title("first AP velocity")

    if saveAs:
        print("saving",os.path.abspath(saveAs))
        plt.savefig(os.path.abspath(saveAs),dpi=dpi)
        return
    if show:
        plot.show()