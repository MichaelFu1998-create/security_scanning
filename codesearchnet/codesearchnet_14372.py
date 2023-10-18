def not_has_branch(branch):
    """Raises `ExistingBranchError` if the specified branch exists."""
    if _has_branch(branch):
        msg = 'Cannot proceed while {} branch exists; remove and try again.'.format(branch)
        raise temple.exceptions.ExistingBranchError(msg)