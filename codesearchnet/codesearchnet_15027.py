def watchdogctl(ctx, kill=False, verbose=True):
    """Control / check a running Sphinx autobuild process."""
    tries = 40 if kill else 0
    cmd = 'lsof -i TCP:{} -s TCP:LISTEN -S -Fp 2>/dev/null'.format(ctx.rituals.docs.watchdog.port)

    pidno = 0
    pidinfo = capture(cmd, ignore_failures=True)
    while pidinfo:
        pidline = next(filter(None, [re.match(r'^p(\d+)$', x) for x in pidinfo.splitlines()]))
        if not pidline:
            raise ValueError("Standard lsof output expected (got {!r})".format(pidinfo))
        pidno = int(pidline.group(1), 10)
        if verbose:
            ctx.run("ps uw {}".format(pidno), echo=False)
            verbose = False

        tries -= 1
        if tries <= 0:
            break
        else:
            try:
                os.kill(pidno, 0)
            #except ProcessLookupError:  # XXX Python3 only
            #    break
            except OSError as exc:  # Python2 has no ProcessLookupError
                if exc.errno == 3:
                    break
                raise
            else:
                notify.info("Killing PID {}".format(pidno))
                ctx.run("kill {}".format(pidno), echo=False)
                time.sleep(.25)

        pid = capture(cmd, ignore_failures=True)

    return pidno