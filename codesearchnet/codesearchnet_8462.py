def runlogs_to_html(run_root):
    """
    Returns content of the given 'fpath' with HTML annotations, currently simply
    a conversion of ANSI color codes to HTML elements
    """

    if not os.path.isdir(run_root):
        return "CANNOT_LOCATE_LOGFILES"

    hook_enter = []
    hook_exit = []
    tcase = []
    for fpath in glob.glob(os.sep.join([run_root, "*.log"])):
        if "exit" in fpath:
            hook_exit.append(fpath)
            continue

        if "hook" in fpath:
            hook_enter.append(fpath)
            continue

        tcase.append(fpath)

    content = ""
    for fpath in hook_enter + tcase + hook_exit:
        content += "# BEGIN: run-log from log_fpath: %s\n" % fpath
        content += open(fpath, "r").read()
        content += "# END: run-log from log_fpath: %s\n\n" % fpath

    return content