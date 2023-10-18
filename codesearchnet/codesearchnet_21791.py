def deactivate():
    '''Deactivates an environment by restoring all env vars to a clean state
    stored prior to activating environments
    '''

    if 'CPENV_ACTIVE' not in os.environ or 'CPENV_CLEAN_ENV' not in os.environ:
        raise EnvironmentError('Can not deactivate environment...')

    utils.restore_env_from_file(os.environ['CPENV_CLEAN_ENV'])