def cmd_events(opts):
    """Get the event log for a given blockade
    """
    config = load_config(opts.config)
    b = get_blockade(config, opts)

    if opts.json:
        outf = None
        _write = puts
        if opts.output is not None:
            outf = open(opts.output, "w")
            _write = outf.write
        try:
            delim = ""
            logs = b.get_audit().read_logs(as_json=False)
            _write('{"events": [')
            _write(os.linesep)
            for l in logs:
                _write(delim + l)
                delim = "," + os.linesep
            _write(os.linesep)
            _write(']}')
        finally:
            if opts.output is not None:
                outf.close()
    else:
        puts(colored.blue(columns(["EVENT",         10],
                                  ["TARGET",        16],
                                  ["STATUS",         8],
                                  ["TIME",          16],
                                  ["MESSAGE",       25])))

        logs = b.get_audit().read_logs(as_json=True)
        for l in logs:
            puts(columns([l['event'],                          10],
                         [str([str(t) for t in l['targets']]), 16],
                         [l['status'],                          8],
                         [str(l['timestamp']),                 16],
                         [l['message'],                        25]))