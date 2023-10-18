def check_subprocess(cmd, source, outname):
    """Run the command to resize the video and remove the output file if the
    processing fails.

    """
    logger = logging.getLogger(__name__)
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    except KeyboardInterrupt:
        logger.debug('Process terminated, removing file %s', outname)
        if os.path.isfile(outname):
            os.remove(outname)
        raise

    if res.returncode:
        logger.debug('STDOUT:\n %s', res.stdout.decode('utf8'))
        logger.debug('STDERR:\n %s', res.stderr.decode('utf8'))
        if os.path.isfile(outname):
            logger.debug('Removing file %s', outname)
            os.remove(outname)
        raise SubprocessException('Failed to process ' + source)