def prompt(prefix=None, colored=True):
    '''Generate a prompt with a given prefix

    linux/osx: [prefix] user@host cwd $
          win: [prefix] cwd:
    '''

    if platform == 'win':
        return '[{0}] $P$G'.format(prefix)
    else:
        if colored:
            return (
                '[{0}] '  # White prefix
                '\\[\\033[01;32m\\]\\u@\\h\\[\\033[00m\\] '  # Green user@host
                '\\[\\033[01;34m\\]\\w $ \\[\\033[00m\\]'  # Blue cwd $
            ).format(prefix)
        return '[{0}] \\u@\\h \\w $ '.format(prefix)