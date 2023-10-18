def main():
    """ Main entry point, expects doctopt arg dict as argd. """
    global DEBUG
    argd = docopt(USAGESTR, version=VERSIONSTR, script=SCRIPT)
    DEBUG = argd['--debug']

    width = parse_int(argd['--width'] or DEFAULT_WIDTH) or 1
    indent = parse_int(argd['--indent'] or (argd['--INDENT'] or 0))
    prepend = ' ' * (indent * 4)
    if prepend and argd['--indent']:
        # Smart indent, change max width based on indention.
        width -= len(prepend)

    userprepend = argd['--prepend'] or (argd['--PREPEND'] or '')
    prepend = ''.join((prepend, userprepend))
    if argd['--prepend']:
        # Smart indent, change max width based on prepended text.
        width -= len(userprepend)
    userappend = argd['--append'] or (argd['--APPEND'] or '')
    if argd['--append']:
        width -= len(userappend)

    if argd['WORDS']:
        # Try each argument as a file name.
        argd['WORDS'] = (
            (try_read_file(w) if len(w) < 256 else w)
            for w in argd['WORDS']
        )
        words = ' '.join((w for w in argd['WORDS'] if w))
    else:
        # No text/filenames provided, use stdin for input.
        words = read_stdin()

    block = FormatBlock(words).iter_format_block(
        chars=argd['--chars'],
        fill=argd['--fill'],
        prepend=prepend,
        strip_first=argd['--stripfirst'],
        append=userappend,
        strip_last=argd['--striplast'],
        width=width,
        newlines=argd['--newlines'],
        lstrip=argd['--lstrip'],
    )

    for i, line in enumerate(block):
        if argd['--enumerate']:
            # Current line number format supports up to 999 lines before
            # messing up. Who would format 1000 lines like this anyway?
            print('{: >3}: {}'.format(i + 1, line))
        else:
            print(line)

    return 0