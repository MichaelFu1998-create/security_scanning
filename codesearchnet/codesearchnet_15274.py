def reset_cleansers(confirm=True):
    """destroys all cleanser slaves and their rollback snapshots, as well as the initial master
    snapshot - this allows re-running the jailhost deployment to recreate fresh cleansers."""

    if value_asbool(confirm) and not yesno("""\nObacht!
            This will destroy any existing and or currently running cleanser jails.
            Are you sure that you want to continue?"""):
        exit("Glad I asked...")

    get_vars()

    cleanser_count = AV['ploy_cleanser_count']
    # make sure no workers interfere:
    fab.run('ezjail-admin stop worker')
    # stop and nuke the cleanser slaves
    for cleanser_index in range(cleanser_count):
        cindex = '{:02d}'.format(cleanser_index + 1)
        fab.run('ezjail-admin stop cleanser_{cindex}'.format(cindex=cindex))
        with fab.warn_only():
            fab.run('zfs destroy tank/jails/cleanser_{cindex}@jdispatch_rollback'.format(cindex=cindex))
            fab.run('ezjail-admin delete -fw cleanser_{cindex}'.format(cindex=cindex))
            fab.run('umount -f /usr/jails/cleanser_{cindex}'.format(cindex=cindex))
            fab.run('rm -rf /usr/jails/cleanser_{cindex}'.format(cindex=cindex))

    with fab.warn_only():
        # remove master snapshot
        fab.run('zfs destroy -R tank/jails/cleanser@clonesource')

        # restart worker and cleanser to prepare for subsequent ansible configuration runs
        fab.run('ezjail-admin start worker')
        fab.run('ezjail-admin stop cleanser')
        fab.run('ezjail-admin start cleanser')