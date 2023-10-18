def rsync_docs():
    """Upload the docs to a remote location via rsync.

    `options.paved.docs.rsync_location`: the target location to rsync files to.

    `options.paved.docs.path`: the path to the Sphinx folder (where the Makefile resides).

    `options.paved.docs.build_rel`: the path of the documentation
        build folder, relative to `options.paved.docs.path`.
    """
    assert options.paved.docs.rsync_location, "Please specify an rsync location in options.paved.docs.rsync_location."
    sh('rsync -ravz %s/ %s/' % (path(options.paved.docs.path) / options.paved.docs.build_rel,
                                options.paved.docs.rsync_location))