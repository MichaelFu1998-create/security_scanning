def soxi(filepath, argument):
    ''' Base call to SoXI.

    Parameters
    ----------
    filepath : str
        Path to audio file.

    argument : str
        Argument to pass to SoXI.

    Returns
    -------
    shell_output : str
        Command line output of SoXI
    '''

    if argument not in SOXI_ARGS:
        raise ValueError("Invalid argument '{}' to SoXI".format(argument))

    args = ['sox', '--i']
    args.append("-{}".format(argument))
    args.append(filepath)

    try:
        shell_output = subprocess.check_output(
            args,
            stderr=subprocess.PIPE
        )
    except CalledProcessError as cpe:
        logger.info("SoXI error message: {}".format(cpe.output))
        raise SoxiError("SoXI failed with exit code {}".format(cpe.returncode))

    shell_output = shell_output.decode("utf-8")

    return str(shell_output).strip('\n')