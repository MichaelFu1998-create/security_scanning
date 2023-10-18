def postprocess(trun):
    """Perform postprocessing of the given test run"""

    plog = []
    plog.append(("trun", process_trun(trun)))

    for tsuite in trun["testsuites"]:
        plog.append(("tsuite", process_tsuite(tsuite)))

        for tcase in tsuite["testcases"]:
            plog.append(("tcase", process_tcase(tcase)))

    for task, success in plog:
        if not success:
            cij.err("rprtr::postprocess: FAILED for %r" % task)

    return sum((success for task, success in plog))