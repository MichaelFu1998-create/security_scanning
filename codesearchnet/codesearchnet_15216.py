def make_df_getter(data_url: str, data_path: str, **kwargs) -> Callable[[Optional[str], bool, bool], pd.DataFrame]:
    """Build a function that handles downloading tabular data and parsing it into a pandas DataFrame.

    :param data_url: The URL of the data
    :param data_path: The path where the data should get stored
    :param kwargs: Any other arguments to pass to :func:`pandas.read_csv`
    """
    download_function = make_downloader(data_url, data_path)

    def get_df(url: Optional[str] = None, cache: bool = True, force_download: bool = False) -> pd.DataFrame:
        """Get the data as a pandas DataFrame.

        :param url: The URL (or file path) to download.
        :param cache: If true, the data is downloaded to the file system, else it is loaded from the internet
        :param force_download: If true, overwrites a previously cached file
        """
        if url is None and cache:
            url = download_function(force_download=force_download)

        return pd.read_csv(
            url or data_url,
            **kwargs
        )

    return get_df