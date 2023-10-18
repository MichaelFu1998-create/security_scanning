def hook_setup(parent, hook_fpath):
    """Setup hook"""

    hook = copy.deepcopy(HOOK)
    hook["name"] = os.path.splitext(os.path.basename(hook_fpath))[0]
    hook["name"] = hook["name"].replace("_enter", "").replace("_exit", "")
    hook["res_root"] = parent["res_root"]
    hook["fpath_orig"] = hook_fpath
    hook["fname"] = "hook_%s" % os.path.basename(hook["fpath_orig"])
    hook["fpath"] = os.sep.join([hook["res_root"], hook["fname"]])
    hook["log_fpath"] = os.sep.join([
        hook["res_root"],
        "%s.log" % hook["fname"]
    ])

    hook["evars"].update(copy.deepcopy(parent["evars"]))

    shutil.copyfile(hook["fpath_orig"], hook["fpath"])

    return hook