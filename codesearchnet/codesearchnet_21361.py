def ensure_remote_branch_is_tracked(branch):
    """Track the specified remote branch if it is not already tracked."""
    if branch == MASTER_BRANCH:
        # We don't need to explicitly track the master branch, so we're done.
        return

    # Ensure the specified branch is in the local branch list.
    output = subprocess.check_output(['git', 'branch', '--list'])
    for line in output.split('\n'):
        if line.strip() == branch:
            # We are already tracking the remote branch
            break
    else:
        # We are not tracking the remote branch, so track it.
        try:
            sys.stdout.write(subprocess.check_output(
                ['git', 'checkout', '--track', 'origin/%s' % branch]))
        except subprocess.CalledProcessError:
            # Bail gracefully.
            raise SystemExit(1)