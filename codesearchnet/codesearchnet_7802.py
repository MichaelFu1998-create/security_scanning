def sox(args):
    '''Pass an argument list to SoX.

    Parameters
    ----------
    args : iterable
        Argument list for SoX. The first item can, but does not
        need to, be 'sox'.

    Returns:
    --------
    status : bool
        True on success.

    '''
    if args[0].lower() != "sox":
        args.insert(0, "sox")
    else:
        args[0] = "sox"

    try:
        logger.info("Executing: %s", ' '.join(args))

        process_handle = subprocess.Popen(
            args, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        out, err = process_handle.communicate()
        out = out.decode("utf-8")
        err = err.decode("utf-8")

        status = process_handle.returncode
        return status, out, err

    except OSError as error_msg:
        logger.error("OSError: SoX failed! %s", error_msg)
    except TypeError as error_msg:
        logger.error("TypeError: %s", error_msg)
    return 1, None, None