def tcase_enter(trun, tsuite, tcase):
    """
    setup res_root and aux_root, log info and run tcase-enter-hooks

    @returns 0 when all hooks succeed, some value othervise
    """
    #pylint: disable=locally-disabled, unused-argument

    if trun["conf"]["VERBOSE"]:
        cij.emph("rnr:tcase:enter")
        cij.emph("rnr:tcase:enter { fname: %r }" % tcase["fname"])
        cij.emph("rnr:tcase:enter { log_fpath: %r }" % tcase["log_fpath"])

    rcode = 0
    for hook in tcase["hooks"]["enter"]:    # tcase ENTER-hooks
        rcode = script_run(trun, hook)
        if rcode:
            break

    if trun["conf"]["VERBOSE"]:
        cij.emph("rnr:tcase:exit: { rcode: %r }" % rcode, rcode)

    return rcode