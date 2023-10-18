def _has_branch(branch):
    """Return True if the target branch exists."""
    ret = temple.utils.shell('git rev-parse --verify {}'.format(branch),
                             stderr=subprocess.DEVNULL,
                             stdout=subprocess.DEVNULL,
                             check=False)
    return ret.returncode == 0