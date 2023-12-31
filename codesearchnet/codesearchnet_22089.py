def ghpages():
    '''Push Sphinx docs to github_ gh-pages branch.

     1. Create file .nojekyll
     2. Push the branch to origin/gh-pages
        after committing using ghp-import_

    Requirements:
     - easy_install ghp-import

    Options:
     - `options.paved.docs.*` is not used
     - `options.sphinx.docroot` is used (default=docs)
     - `options.sphinx.builddir` is used (default=.build)

    .. warning::
        This will DESTROY your gh-pages branch.
        If you love it, you'll want to take backups
        before playing with this. This script assumes
        that gh-pages is 100% derivative. You should
        never edit files in your gh-pages branch by hand
        if you're using this script because you will
        lose your work.

    .. _github: https://github.com
    .. _ghp-import: https://github.com/davisp/ghp-import
    '''

    # copy from paver
    opts = options
    docroot = path(opts.get('docroot', 'docs'))
    if not docroot.exists():
        raise BuildFailure("Sphinx documentation root (%s) does not exist."
                           % docroot)
    builddir = docroot / opts.get("builddir", ".build")
    # end of copy

    builddir=builddir / 'html'
    if not builddir.exists():
        raise BuildFailure("Sphinx build directory (%s) does not exist."
                           % builddir)

    nojekyll = path(builddir) / '.nojekyll'
    nojekyll.touch()

    sh('ghp-import -p %s' % (builddir))