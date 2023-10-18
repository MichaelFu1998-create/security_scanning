def add_file_normal(f, targetdir, generator,script, source):
    """
    Add a normal file including its source
    """

    basename = os.path.basename(f)
    if targetdir != ".":
        relativepath = os.path.join(targetdir, basename)
    else:
        relativepath = basename

    relpath = os.path.relpath(f, os.getcwd())
    filetype = 'data'
    if script:
        filetype = 'script'
        if generator:
            filetype = 'generator'

    update = OrderedDict([
        ('type', filetype),
        ('generator', generator),
        ('relativepath', relativepath),
        ('content', ""),
        ('source', source),
        ('localfullpath', f),
        ('localrelativepath', relpath)
    ])

    update = annotate_record(update)

    return (basename, update)