def stats_first(abf):
    """provide all stats on the first AP."""
    msg=""
    for sweep in range(abf.sweeps):
        for AP in abf.APs[sweep]:
            for key in sorted(AP.keys()):
                if key[-1] is "I" or key[-2:] in ["I1","I2"]:
                    continue
                msg+="%s = %s\n"%(key,AP[key])
            return msg