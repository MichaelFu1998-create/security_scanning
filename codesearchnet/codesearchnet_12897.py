def save_json2(data):
    """ save to json."""

    ## convert everything to dicts
    ## skip _ipcluster cuz it's made new.
    datadict = OrderedDict([
        ("outfiles", data.__dict__["outfiles"]),
        ("stats_files", dict(data.__dict__["stats_files"])),
        ("stats_dfs", data.__dict__["stats_dfs"])
        ])