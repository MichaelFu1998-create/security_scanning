def pyflakes():
    '''passive check of python programs by pyflakes.

    requirements:
     - pyflakes_ should be installed. ``easy_install pyflakes``

    options.paved.pycheck.pyflakes.param

    .. _pyflakes: http://pypi.python.org/pypi/pyflakes
    '''

    # filter out  subpackages
    packages = [x for x in options.setup.packages if '.' not in x]

    sh('pyflakes {param} {files}'.format(param=options.paved.pycheck.pyflakes.param, files=' '.join(packages)))