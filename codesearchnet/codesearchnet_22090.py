def showhtml():
    """Open your web browser and display the generated html documentation.
    """
    import webbrowser

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

    webbrowser.open(builddir / 'index.html')