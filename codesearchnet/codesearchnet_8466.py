def process_tcase(tcase):
    """Goes through the trun and processes "run.log" """

    tcase["src_content"] = src_to_html(tcase["fpath"])
    tcase["log_content"] = runlogs_to_html(tcase["res_root"])
    tcase["aux_list"] = aux_listing(tcase["aux_root"])
    tcase["descr_short"], tcase["descr_long"] = tcase_parse_descr(tcase)
    tcase["hnames"] = extract_hook_names(tcase)

    return True