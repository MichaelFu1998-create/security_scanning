def play(args):
    '''Pass an argument list to play.

    Parameters
    ----------
    args : iterable
        Argument list for play. The first item can, but does not
        need to, be 'play'.

    Returns:
    --------
    status : bool
        True on success.

    '''
    if args[0].lower() != "play":
        args.insert(0, "play")
    else:
        args[0] = "play"

    try:
        logger.info("Executing: %s", " ".join(args))
        process_handle = subprocess.Popen(
            args, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        status = process_handle.wait()
        if process_handle.stderr is not None:
            logger.info(process_handle.stderr)

        if status == 0:
            return True
        else:
            logger.info("Play returned with error code %s", status)
            return False
    except OSError as error_msg:
        logger.error("OSError: Play failed! %s", error_msg)
    except TypeError as error_msg:
        logger.error("TypeError: %s", error_msg)
    return False