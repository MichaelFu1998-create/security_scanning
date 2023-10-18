def main(args):
    """Main entry point"""

    trun = cij.runner.trun_from_file(args.trun_fpath)

    rehome(trun["conf"]["OUTPUT"], args.output, trun)

    postprocess(trun)

    cij.emph("main: reports are uses tmpl_fpath: %r" % args.tmpl_fpath)
    cij.emph("main: reports are here args.output: %r" % args.output)

    html_fpath = os.sep.join([args.output, "%s.html" % args.tmpl_name])
    cij.emph("html_fpath: %r" % html_fpath)
    try:                                    # Create and store HTML report
        with open(html_fpath, 'w') as html_file:
            html_file.write(dset_to_html(trun, args.tmpl_fpath))
    except (IOError, OSError, ValueError) as exc:
        import traceback
        traceback.print_exc()
        cij.err("rprtr:main: exc: %s" % exc)
        return 1

    return 0