def compute_exit_code(config, exception=None):
    """Compute an exit code for mutmut mutation testing

    The following exit codes are available for mutmut:
     * 0 if all mutants were killed (OK_KILLED)
     * 1 if a fatal error occurred
     * 2 if one or more mutants survived (BAD_SURVIVED)
     * 4 if one or more mutants timed out (BAD_TIMEOUT)
     * 8 if one or more mutants caused tests to take twice as long (OK_SUSPICIOUS)

     Exit codes 1 to 8 will be bit-ORed so that it is possible to know what
     different mutant statuses occurred during mutation testing.

    :param exception:
    :type exception: Exception
    :param config:
    :type config: Config

    :return: integer noting the exit code of the mutation tests.
    :rtype: int
    """
    code = 0
    if exception is not None:
        code = code | 1
    if config.surviving_mutants > 0:
        code = code | 2
    if config.surviving_mutants_timeout > 0:
        code = code | 4
    if config.suspicious_mutants > 0:
        code = code | 8
    return code