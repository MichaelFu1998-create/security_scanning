def capture(cmd, **kw):
    """Run a command and return its stripped captured output."""
    kw = kw.copy()
    kw['hide'] = 'out'
    if not kw.get('echo', False):
        kw['echo'] = False
    ignore_failures = kw.pop('ignore_failures', False)
    try:
        return invoke_run(cmd, **kw).stdout.strip()
    except exceptions.Failure as exc:
        if not ignore_failures:
            notify.error("Command `{}` failed with RC={}!".format(cmd, exc.result.return_code,))
            raise