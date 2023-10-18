def sphinx_make(*targets):
    """Call the Sphinx Makefile with the specified targets.

    `options.paved.docs.path`: the path to the Sphinx folder (where the Makefile resides).
    """
    sh('make %s' % ' '.join(targets), cwd=options.paved.docs.path)