def hooks_setup(trun, parent, hnames=None):
    """
    Setup test-hooks
    @returns dict of hook filepaths {"enter": [], "exit": []}
    """

    hooks = {
        "enter": [],
        "exit": []
    }

    if hnames is None:       # Nothing to do, just return the struct
        return hooks

    for hname in hnames:      # Fill out paths
        for med in HOOK_PATTERNS:
            for ptn in HOOK_PATTERNS[med]:
                fpath = os.sep.join([trun["conf"]["HOOKS"], ptn % hname])
                if not os.path.exists(fpath):
                    continue

                hook = hook_setup(parent, fpath)
                if not hook:
                    continue

                hooks[med].append(hook)

        if not hooks["enter"] + hooks["exit"]:
            cij.err("rnr:hooks_setup:FAIL { hname: %r has no files }" % hname)
            return None

    return hooks