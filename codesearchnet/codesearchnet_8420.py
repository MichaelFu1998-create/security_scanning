def trun_enter(trun):
    """Triggers when entering the given testrun"""

    if trun["conf"]["VERBOSE"]:
        cij.emph("rnr:trun::enter")

    trun["stamp"]["begin"] = int(time.time())     # Record start timestamp

    rcode = 0
    for hook in trun["hooks"]["enter"]:     # ENTER-hooks
        rcode = script_run(trun, hook)
        if rcode:
            break

    if trun["conf"]["VERBOSE"]:
        cij.emph("rnr:trun::enter { rcode: %r }" % rcode, rcode)

    return rcode