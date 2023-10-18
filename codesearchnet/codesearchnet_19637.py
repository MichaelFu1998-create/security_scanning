def git_tag(tag):
    """Tags the current version."""
    print('Tagging "{}"'.format(tag))
    msg = '"Released version {}"'.format(tag)
    Popen(['git', 'tag', '-s', '-m', msg, tag]).wait()