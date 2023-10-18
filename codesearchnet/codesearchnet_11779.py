def reboot_or_dryrun(*args, **kwargs):
    """
    An improved version of fabric.operations.reboot with better error handling.
    """
    from fabric.state import connections

    verbose = get_verbose()

    dryrun = get_dryrun(kwargs.get('dryrun'))

    # Use 'wait' as max total wait time
    kwargs.setdefault('wait', 120)
    wait = int(kwargs['wait'])

    command = kwargs.get('command', 'reboot')

    now = int(kwargs.get('now', 0))
    print('now:', now)
    if now:
        command += ' now'

    # Shorter timeout for a more granular cycle than the default.
    timeout = int(kwargs.get('timeout', 30))

    reconnect_hostname = kwargs.pop('new_hostname', env.host_string)

    if 'dryrun' in kwargs:
        del kwargs['dryrun']

    if dryrun:
        print('%s sudo: %s' % (render_command_prefix(), command))
    else:
        if is_local():
            if raw_input('reboot localhost now? ').strip()[0].lower() != 'y':
                return

        attempts = int(round(float(wait) / float(timeout)))
        # Don't bleed settings, since this is supposed to be self-contained.
        # User adaptations will probably want to drop the "with settings()" and
        # just have globally set timeout/attempts values.
        with settings(warn_only=True):
            _sudo(command)

        env.host_string = reconnect_hostname
        success = False
        for attempt in xrange(attempts):

            # Try to make sure we don't slip in before pre-reboot lockdown
            if verbose:
                print('Waiting for %s seconds, wait %i of %i' % (timeout, attempt+1, attempts))
            time.sleep(timeout)

            # This is actually an internal-ish API call, but users can simply drop
            # it in real fabfile use -- the next run/sudo/put/get/etc call will
            # automatically trigger a reconnect.
            # We use it here to force the reconnect while this function is still in
            # control and has the above timeout settings enabled.
            try:
                if verbose:
                    print('Reconnecting to:', env.host_string)
                # This will fail until the network interface comes back up.
                connections.connect(env.host_string)
                # This will also fail until SSH is running again.
                with settings(timeout=timeout):
                    _run('echo hello')
                success = True
                break
            except Exception as e:
                print('Exception:', e)

        if not success:
            raise Exception('Reboot failed or took longer than %s seconds.' % wait)