def proto_01_12_steps025(abf=exampleABF):
    """IC steps. Use to determine gain function."""
    swhlab.ap.detect(abf)
    standard_groupingForInj(abf,200)

    for feature in ['freq','downslope']:
        swhlab.ap.plot_values(abf,feature,continuous=False) #plot AP info
        swhlab.plot.save(abf,tag='A_'+feature)

    swhlab.plot.gain(abf) #easy way to do a gain function!
    swhlab.plot.save(abf,tag='05-gain')