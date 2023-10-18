def frameAndSave(abf,tag="",dataType="plot",saveAsFname=False,closeWhenDone=True):
    """
    frame the current matplotlib plot with ABF info, and optionally save it.
    Note that this is entirely independent of the ABFplot class object.
    if saveImage is False, show it instead.

    Datatype should be:
        * plot
        * experiment
    """
    print("closeWhenDone",closeWhenDone)
    plt.tight_layout()
    plt.subplots_adjust(top=.93,bottom =.07)
    plt.annotate(tag,(.01,.99),xycoords='figure fraction',ha='left',va='top',family='monospace',size=10,alpha=.5)
    msgBot="%s [%s]"%(abf.ID,abf.protocomment)
    plt.annotate(msgBot,(.01,.01),xycoords='figure fraction',ha='left',va='bottom',family='monospace',size=10,alpha=.5)
    fname=tag.lower().replace(" ",'_')+".jpg"
    fname=dataType+"_"+fname
    plt.tight_layout()
    if IMAGE_SAVE:
        abf.log.info("saving [%s]",fname)
        try:
            if saveAsFname:
                saveAs=os.path.abspath(saveAsFname)
            else:
                saveAs=os.path.abspath(abf.outPre+fname)
            if not os.path.exists(abf.outFolder):
                os.mkdir(abf.outFolder)
            plt.savefig(saveAs)
        except Exception as E:
            abf.log.error("saving [%s] failed! 'pip install pillow'?",fname)
            print(E)
    if IMAGE_SHOW==True:
        if closeWhenDone==False:
            print("NOT SHOWING (because closeWhenDone==True and showing would mess things up)")
        else:
            abf.log.info("showing [%s]",fname)
            plt.show()
    if closeWhenDone:
        print("closing figure")
        plt.close('all')