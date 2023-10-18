def reset_jails(confirm=True, keep_cleanser_master=True):
    """ stops, deletes and re-creates all jails.
    since the cleanser master is rather large, that one is omitted by default.
    """
    if value_asbool(confirm) and not yesno("""\nObacht!
            This will destroy all existing and or currently running jails on the host.
            Are you sure that you want to continue?"""):
        exit("Glad I asked...")

    reset_cleansers(confirm=False)

    jails = ['appserver', 'webserver', 'worker']
    if not value_asbool(keep_cleanser_master):
        jails.append('cleanser')

    with fab.warn_only():
        for jail in jails:
            fab.run('ezjail-admin delete -fw {jail}'.format(jail=jail))
        # remove authorized keys for no longer existing key (they are regenerated for each new worker)
        fab.run('rm /usr/jails/cleanser/usr/home/cleanser/.ssh/authorized_keys')