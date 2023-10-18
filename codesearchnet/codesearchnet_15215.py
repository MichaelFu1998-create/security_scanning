def make_downloader(url: str, path: str) -> Callable[[bool], str]:  # noqa: D202
    """Make a function that downloads the data for you, or uses a cached version at the given path.

    :param url: The URL of some data
    :param path: The path of the cached data, or where data is cached if it does not already exist
    :return: A function that downloads the data and returns the path of the data
    """

    def download_data(force_download: bool = False) -> str:
        """Download the data.

        :param force_download: If true, overwrites a previously cached file
        """
        if os.path.exists(path) and not force_download:
            log.info('using cached data at %s', path)
        else:
            log.info('downloading %s to %s', url, path)
            urlretrieve(url, path)

        return path

    return download_data