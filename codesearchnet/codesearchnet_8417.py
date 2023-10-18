def tcase_exit(trun, tsuite, tcase):
    """..."""
    #pylint: disable=locally-disabled, unused-argument

    if trun["conf"]["VERBOSE"]:
        cij.emph("rnr:tcase:exit { fname: %r }" % tcase["fname"])

    rcode = 0
    for hook in reversed(tcase["hooks"]["exit"]):    # tcase EXIT-hooks
        rcode = script_run(trun, hook)
        if rcode:
            break

    if trun["conf"]["VERBOSE"]:
        cij.emph("rnr:tcase:exit { rcode: %r }" % rcode, rcode)

    return rcode