def main(conf):
    """CIJ Test Runner main entry point"""

    fpath = yml_fpath(conf["OUTPUT"])
    if os.path.exists(fpath):   # YAML exists, we exit, it might be RUNNING!
        cij.err("main:FAILED { fpath: %r }, exists" % fpath)
        return 1

    trun = trun_setup(conf)         # Construct 'trun' from 'conf'
    if not trun:
        return 1

    trun_to_file(trun)              # Persist trun
    trun_emph(trun)                 # Print trun before run

    tr_err = 0
    tr_ent_err = trun_enter(trun)
    for tsuite in (ts for ts in trun["testsuites"] if not tr_ent_err):

        ts_err = 0
        ts_ent_err = tsuite_enter(trun, tsuite)
        for tcase in (tc for tc in tsuite["testcases"] if not ts_ent_err):

            tc_err = tcase_enter(trun, tsuite, tcase)
            if not tc_err:
                tc_err += script_run(trun, tcase)
                tc_err += tcase_exit(trun, tsuite, tcase)

            tcase["status"] = "FAIL" if tc_err else "PASS"

            trun["progress"][tcase["status"]] += 1  # Update progress
            trun["progress"]["UNKN"] -= 1

            ts_err += tc_err                        # Accumulate errors

            trun_to_file(trun)                      # Persist trun

        if not ts_ent_err:
            ts_err += tsuite_exit(trun, tsuite)

        ts_err += ts_ent_err                        # Accumulate errors
        tr_err += ts_err

        tsuite["status"] = "FAIL" if ts_err else "PASS"

        cij.emph("rnr:tsuite %r" % tsuite["status"], tsuite["status"] != "PASS")

    if not tr_ent_err:
        trun_exit(trun)

    tr_err += tr_ent_err
    trun["status"] = "FAIL" if tr_err else "PASS"

    trun["stamp"]["end"] = int(time.time()) + 1         # END STAMP
    trun_to_file(trun)                                  # PERSIST

    cij.emph("rnr:main:progress %r" % trun["progress"])
    cij.emph("rnr:main:trun %r" % trun["status"], trun["status"] != "PASS")

    return trun["progress"]["UNKN"] + trun["progress"]["FAIL"]