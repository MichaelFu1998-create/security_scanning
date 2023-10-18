def ensure_pandoc(func):
    """Decorate a function that uses pypandoc to ensure that pandoc is
    installed if necessary.
    """
    logger = logging.getLogger(__name__)

    @functools.wraps(func)
    def _install_and_run(*args, **kwargs):
        try:
            # First try to run pypandoc function
            result = func(*args, **kwargs)
        except OSError:
            # Install pandoc and retry
            message = "pandoc needed but not found. Now installing it for you."
            logger.warning(message)
            # This version of pandoc is known to be compatible with both
            # pypandoc.download_pandoc and the functionality that
            # lsstprojectmeta needs. Travis CI tests are useful for ensuring
            # download_pandoc works.
            pypandoc.download_pandoc(version='1.19.1')
            logger.debug("pandoc download complete")

            result = func(*args, **kwargs)

        return result

    return _install_and_run