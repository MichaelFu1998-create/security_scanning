def trun_setup(conf):
    """
    Setup the testrunner data-structure, embedding the parsed environment
    variables and command-line arguments and continues with setup for testplans,
    testsuites, and testcases
    """

    declr = None
    try:
        with open(conf["TESTPLAN_FPATH"]) as declr_fd:
            declr = yaml.safe_load(declr_fd)
    except AttributeError as exc:
        cij.err("rnr: %r" % exc)

    if not declr:
        return None

    trun = copy.deepcopy(TRUN)
    trun["ver"] = cij.VERSION

    trun["conf"] = copy.deepcopy(conf)
    trun["res_root"] = conf["OUTPUT"]
    trun["aux_root"] = os.sep.join([trun["res_root"], "_aux"])
    trun["evars"].update(copy.deepcopy(declr.get("evars", {})))

    os.makedirs(trun["aux_root"])

    hook_names = declr.get("hooks", [])
    if "lock" not in hook_names:
        hook_names = ["lock"] + hook_names

    if hook_names[0] != "lock":
        return None

    # Setup top-level hooks
    trun["hooks"] = hooks_setup(trun, trun, hook_names)

    for enum, declr in enumerate(declr["testsuites"]):  # Setup testsuites
        tsuite = tsuite_setup(trun, declr, enum)
        if tsuite is None:
            cij.err("main::FAILED: setting up tsuite: %r" % tsuite)
            return 1

        trun["testsuites"].append(tsuite)
        trun["progress"]["UNKN"] += len(tsuite["testcases"])

    return trun