def main(branch):
    """Checkout, update and branch from the specified branch."""
    try:
        # Ensure that we're in a git repository. This command is silent unless
        # you're not actually in a git repository, in which case, you receive a
        # "Not a git repository" error message.
        output = subprocess.check_output(['git', 'rev-parse']).decode('utf-8')
        sys.stdout.write(output)
    except subprocess.CalledProcessError:
        # Bail if we're not in a git repository.
        return

    # This behavior ensures a better user experience for those that aren't
    # intimately familiar with git.
    ensure_remote_branch_is_tracked(branch)

    # Switch to the specified branch and update it.
    subprocess.check_call(['git', 'checkout', '--quiet', branch])

    # Pulling is always safe here, because we never commit to this branch.
    subprocess.check_call(['git', 'pull', '--quiet'])

    # Checkout the top commit in the branch, effectively going "untracked."
    subprocess.check_call(['git', 'checkout', '--quiet', '%s~0' % branch])

    # Clean up the repository of Python cruft. Because we've just switched
    # branches and compiled Python files should not be version controlled,
    # there are likely leftover compiled Python files sitting on disk which may
    # confuse some tools, such as sqlalchemy-migrate.
    subprocess.check_call(['find', '.', '-name', '"*.pyc"', '-delete'])

    # For the sake of user experience, give some familiar output.
    print('Your branch is up to date with branch \'origin/%s\'.' % branch)