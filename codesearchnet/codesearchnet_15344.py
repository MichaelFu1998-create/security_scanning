def version():
    """Return version string."""
    with io.open('pgmagick/_version.py') as input_file:
        for line in input_file:
            if line.startswith('__version__'):
                return ast.parse(line).body[0].value.s