def print_message(message=None):
    """Print message via ``subprocess.call`` function.

    This helps to ensure consistent output and avoid situations where print
    messages actually shown after messages from all inner threads.

    :param message: Text message to print.
    """
    kwargs = {'stdout': sys.stdout,
              'stderr': sys.stderr,
              'shell': True}
    return subprocess.call('echo "{0}"'.format(message or ''), **kwargs)