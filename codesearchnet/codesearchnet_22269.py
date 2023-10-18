def check_environment(target, label):
    """
    Performs some environment checks prior to the program's execution
    """
    if not git.exists():
        click.secho('You must have git installed to use yld.', fg='red')
        sys.exit(1)

    if not os.path.isdir('.git'):
        click.secho('You must cd into a git repository to use yld.', fg='red')
        sys.exit(1)

    if not git.is_committed():
        click.secho('You must commit or stash your work before proceeding.',
                    fg='red')
        sys.exit(1)

    if target is None and label is None:
        click.secho('You must specify either a target or a label.', fg='red')
        sys.exit(1)