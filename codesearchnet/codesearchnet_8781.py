def on_init(app):  # pylint: disable=unused-argument
    """
    Run sphinx-apidoc after Sphinx initialization.

    Read the Docs won't run tox or custom shell commands, so we need this to
    avoid checking in the generated reStructuredText files.
    """
    docs_path = os.path.abspath(os.path.dirname(__file__))
    root_path = os.path.abspath(os.path.join(docs_path, '..'))
    apidoc_path = 'sphinx-apidoc'
    if hasattr(sys, 'real_prefix'):  # Check to see if we are in a virtualenv
        # If we are, assemble the path manually
        bin_path = os.path.abspath(os.path.join(sys.prefix, 'bin'))
        apidoc_path = os.path.join(bin_path, apidoc_path)
    check_call([apidoc_path, '-o', docs_path, os.path.join(root_path, 'enterprise'),
                os.path.join(root_path, 'enterprise/migrations')])