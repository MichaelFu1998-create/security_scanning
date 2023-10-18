def is_git_repo(path):
    '''Returns True if path is a git repository.'''

    if path.startswith('git@') or path.startswith('https://'):
        return True

    if os.path.exists(unipath(path, '.git')):
        return True

    return False