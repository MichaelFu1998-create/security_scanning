def tsuite_setup(trun, declr, enum):
    """
    Creates and initialized a TESTSUITE struct and site-effects such as creating
    output directories and forwarding initialization of testcases
    """

    suite = copy.deepcopy(TESTSUITE)  # Setup the test-suite

    suite["name"] = declr.get("name")
    if suite["name"] is None:
        cij.err("rnr:tsuite_setup: no testsuite is given")
        return None

    suite["alias"] = declr.get("alias")
    suite["ident"] = "%s_%d" % (suite["name"], enum)

    suite["res_root"] = os.sep.join([trun["conf"]["OUTPUT"], suite["ident"]])
    suite["aux_root"] = os.sep.join([suite["res_root"], "_aux"])

    suite["evars"].update(copy.deepcopy(trun["evars"]))
    suite["evars"].update(copy.deepcopy(declr.get("evars", {})))

    # Initialize
    os.makedirs(suite["res_root"])
    os.makedirs(suite["aux_root"])

    # Setup testsuite-hooks
    suite["hooks"] = hooks_setup(trun, suite, declr.get("hooks"))

    # Forward from declaration
    suite["hooks_pr_tcase"] = declr.get("hooks_pr_tcase", [])

    suite["fname"] = "%s.suite" % suite["name"]
    suite["fpath"] = os.sep.join([trun["conf"]["TESTSUITES"], suite["fname"]])

    #
    # Load testcases from .suite file OR from declaration
    #
    tcase_fpaths = []                               # Load testcase fpaths
    if os.path.exists(suite["fpath"]):              # From suite-file
        suite_lines = (
            l.strip() for l in open(suite["fpath"]).read().splitlines()
        )
        tcase_fpaths.extend(
            (l for l in suite_lines if len(l) > 1 and l[0] != "#")
        )
    else:                                           # From declaration
        tcase_fpaths.extend(declr.get("testcases", []))

    # NOTE: fix duplicates; allow them
    # NOTE: Currently hot-fixed here
    if len(set(tcase_fpaths)) != len(tcase_fpaths):
        cij.err("rnr:suite: failed: duplicate tcase in suite not supported")
        return None

    for tcase_fname in tcase_fpaths:                # Setup testcases
        tcase = tcase_setup(trun, suite, tcase_fname)
        if not tcase:
            cij.err("rnr:suite: failed: tcase_setup")
            return None

        suite["testcases"].append(tcase)

    return suite