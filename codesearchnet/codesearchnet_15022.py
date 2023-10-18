def run(cmd, **kw):
    """Run a command and flush its output."""
    kw = kw.copy()
    kw.setdefault('warn', False)  # make extra sure errors don't get silenced

    report_error = kw.pop('report_error', True)
    runner = kw.pop('runner', invoke_run)

    try:
        return runner(cmd, **kw)
    except exceptions.Failure as exc:
        sys.stdout.flush()
        sys.stderr.flush()
        if report_error:
            notify.error("Command `{}` failed with RC={}!".format(cmd, exc.result.return_code,))
        raise
    finally:
        sys.stdout.flush()
        sys.stderr.flush()