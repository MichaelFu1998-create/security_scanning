def process_tsuite(tsuite):
    """Goes through the tsuite and processes "*.log" """

    # scoop of output from all run-logs

    tsuite["log_content"] = runlogs_to_html(tsuite["res_root"])
    tsuite["aux_list"] = aux_listing(tsuite["aux_root"])
    tsuite["hnames"] = extract_hook_names(tsuite)

    return True