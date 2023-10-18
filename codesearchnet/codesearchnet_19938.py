def proto_IC_ramp_gain(abf=exampleABF):
    """increasing ramps in (?) pA steps."""
    standard_inspect(abf)
    swhlab.ap.detect(abf)

    swhlab.ap.check_AP_raw(abf) #show overlayed first few APs
    swhlab.plot.save(abf,tag="01-raw",resize=False)
    swhlab.ap.check_AP_deriv(abf) #show overlayed first few APs
    swhlab.plot.save(abf,tag="02-deriv")
    swhlab.ap.check_AP_phase(abf) #show overlayed first few APs
    swhlab.plot.save(abf,tag="03-phase")

    swhlab.ap.plot_values(abf,'freq',continuous=True) #plot AP info
    pylab.subplot(211)
    pylab.axhline(40,color='r',lw=2,ls="--",alpha=.2)
    swhlab.plot.save(abf,tag='04-freq')

    swhlab.ap.plot_values(abf,'downslope',continuous=True) #plot AP info
    pylab.subplot(211)
    pylab.axhline(-100,color='r',lw=2,ls="--",alpha=.2)
    swhlab.plot.save(abf,tag='04-downslope')