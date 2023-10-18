async def _download_text(url, session):
    """Asynchronously request a URL and get the encoded text content of the
    body.

    Parameters
    ----------
    url : `str`
        URL to download.
    session : `aiohttp.ClientSession`
        An open aiohttp session.

    Returns
    -------
    content : `str`
        Content downloaded from the URL.
    """
    logger = logging.getLogger(__name__)
    async with session.get(url) as response:
        # aiohttp decodes the content to a Python string
        logger.info('Downloading %r', url)
        return await response.text()