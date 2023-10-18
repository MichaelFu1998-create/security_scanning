def proto_01_11_rampStep(abf=exampleABF):
    """each sweep is a ramp (of set size) which builds on the last sweep.
    Used for detection of AP properties from first few APs."""
    standard_inspect(abf)
    swhlab.ap.detect(abf)
    swhlab.ap.check_sweep(abf) #eyeball how well event detection worked
    swhlab.plot.save(abf,tag="check")
    swhlab.ap.check_AP_raw(abf) #show overlayed first few APs
    swhlab.plot.save(abf,tag="raw",resize=False)
    swhlab.ap.check_AP_deriv(abf) #show overlayed first few APs
    swhlab.plot.save(abf,tag="deriv")
    swhlab.ap.check_AP_phase(abf) #show overlayed first few APs
    swhlab.plot.save(abf,tag="phase")
    for feature in ['downslope','freq']:
        swhlab.ap.plot_values(abf,feature,continuous=True) #plot AP info
        swhlab.plot.save(abf,tag=feature)