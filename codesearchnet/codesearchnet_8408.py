def script_run(trun, script):
    """Execute a script or testcase"""

    if trun["conf"]["VERBOSE"]:
        cij.emph("rnr:script:run { script: %s }" % script)
        cij.emph("rnr:script:run:evars: %s" % script["evars"])

    launchers = {
        ".py": "python",
        ".sh": "source"
    }

    ext = os.path.splitext(script["fpath"])[-1]
    if not ext in launchers.keys():
        cij.err("rnr:script:run { invalid script[\"fpath\"]: %r }" % script["fpath"])
        return 1

    launch = launchers[ext]

    with open(script["log_fpath"], "a") as log_fd:
        log_fd.write("# script_fpath: %r\n" % script["fpath"])
        log_fd.flush()

        bgn = time.time()
        cmd = [
            'bash', '-c',
            'CIJ_ROOT=$(cij_root) && '
            'source $CIJ_ROOT/modules/cijoe.sh && '
            'source %s && '
            'CIJ_TEST_RES_ROOT="%s" %s %s ' % (
                trun["conf"]["ENV_FPATH"],
                script["res_root"],
                launch,
                script["fpath"]
            )
        ]
        if trun["conf"]["VERBOSE"] > 1:
            cij.emph("rnr:script:run { cmd: %r }" % " ".join(cmd))

        evars = os.environ.copy()
        evars.update({k: str(script["evars"][k]) for k in script["evars"]})

        process = Popen(
            cmd,
            stdout=log_fd,
            stderr=STDOUT,
            cwd=script["res_root"],
            env=evars
        )
        process.wait()

        script["rcode"] = process.returncode
        script["wallc"] = time.time() - bgn

    if trun["conf"]["VERBOSE"]:
        cij.emph("rnr:script:run { wallc: %02f }" % script["wallc"])
        cij.emph(
            "rnr:script:run { rcode: %r } " % script["rcode"],
            script["rcode"]
        )

    return script["rcode"]