def run(*args, **kwargs):
    '''Returns True if successful, False if failure'''

    kwargs.setdefault('env', os.environ)
    kwargs.setdefault('shell', True)

    try:
        subprocess.check_call(' '.join(args), **kwargs)
        return True
    except subprocess.CalledProcessError:
        logger.debug('Error running: {}'.format(args))
        return False