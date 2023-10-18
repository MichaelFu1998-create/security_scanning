def tcase_setup(trun, parent, tcase_fname):
    """
    Create and initialize a testcase
    """
    #pylint: disable=locally-disabled, unused-argument

    case = copy.deepcopy(TESTCASE)

    case["fname"] = tcase_fname
    case["fpath_orig"] = os.sep.join([trun["conf"]["TESTCASES"], case["fname"]])

    if not os.path.exists(case["fpath_orig"]):
        cij.err('rnr:tcase_setup: !case["fpath_orig"]: %r' % case["fpath_orig"])
        return None

    case["name"] = os.path.splitext(case["fname"])[0]
    case["ident"] = "/".join([parent["ident"], case["fname"]])

    case["res_root"] = os.sep.join([parent["res_root"], case["fname"]])
    case["aux_root"] = os.sep.join([case["res_root"], "_aux"])
    case["log_fpath"] = os.sep.join([case["res_root"], "run.log"])

    case["fpath"] = os.sep.join([case["res_root"], case["fname"]])

    case["evars"].update(copy.deepcopy(parent["evars"]))

    # Initalize
    os.makedirs(case["res_root"])                       # Create DIRS
    os.makedirs(case["aux_root"])
    shutil.copyfile(case["fpath_orig"], case["fpath"])  # Copy testcase

    # Initialize hooks
    case["hooks"] = hooks_setup(trun, case, parent.get("hooks_pr_tcase"))

    return case