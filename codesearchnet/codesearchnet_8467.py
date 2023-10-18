def process_trun(trun):
    """Goes through the trun and processes "run.log" """

    trun["log_content"] = runlogs_to_html(trun["res_root"])
    trun["aux_list"] = aux_listing(trun["aux_root"])
    trun["hnames"] = extract_hook_names(trun)

    return True