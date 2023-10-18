def annotate(abf):
    """stamp the bottom with file info."""
    msg="SWHLab %s "%str(swhlab.VERSION)
    msg+="ID:%s "%abf.ID
    msg+="CH:%d "%abf.channel
    msg+="PROTOCOL:%s "%abf.protoComment
    msg+="COMMAND: %d%s "%(abf.holding,abf.units)
    msg+="GENERATED:%s "%'{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    pylab.annotate(msg,(.001,.001),xycoords='figure fraction',ha='left',
                   va='bottom',color='#999999',family='monospace',size=8,
                   weight='bold')
    if abf.nADC>1:
        msg="Ch %d/%d"%(abf.channel+1,abf.nADC)
        pylab.annotate(msg,(.01,.99),xycoords='figure fraction',ha='left',
                       va='top',color='#FF0000',family='monospace',size=12,
                       weight='bold')