def _increase_file_handle_limit():
    """Raise the open file handles permitted by the Dusty daemon process
    and its child processes. The number we choose here needs to be within
    the OS X default kernel hard limit, which is 10240."""
    logging.info('Increasing file handle limit to {}'.format(constants.FILE_HANDLE_LIMIT))
    resource.setrlimit(resource.RLIMIT_NOFILE,
                       (constants.FILE_HANDLE_LIMIT, resource.RLIM_INFINITY))