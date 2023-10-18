def sloccount():
    '''Print "Source Lines of Code" and export to file.

    Export is hudson_ plugin_ compatible: sloccount.sc

    requirements:
     - sloccount_ should be installed.
     - tee and pipes are used

    options.paved.pycheck.sloccount.param

    .. _sloccount: http://www.dwheeler.com/sloccount/
    .. _hudson: http://hudson-ci.org/
    .. _plugin: http://wiki.hudson-ci.org/display/HUDSON/SLOCCount+Plugin
    '''

    # filter out  subpackages
    setup = options.get('setup')
    packages = options.get('packages') if setup else None

    if packages:
        dirs = [x for x in packages if '.' not in x]
    else:
        dirs = ['.']

    # sloccount has strange behaviour with directories,
    # can cause exception in hudson sloccount plugin.
    # Better to call it with file list
    ls=[]
    for d in dirs:
        ls += list(path(d).walkfiles())
    #ls=list(set(ls))
    files=' '.join(ls)
    param=options.paved.pycheck.sloccount.param
    sh('sloccount {param} {files} | tee sloccount.sc'.format(param=param, files=files))