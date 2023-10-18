def _get_current_branch():
    """Determine the current git branch"""
    result = temple.utils.shell('git rev-parse --abbrev-ref HEAD', stdout=subprocess.PIPE)
    return result.stdout.decode('utf8').strip()