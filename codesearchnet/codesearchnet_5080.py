def curated(name):
    """Download and return a path to a sample that is curated by the PyAV developers.

    Data is handled by :func:`cached_download`.

    """
    return cached_download('https://docs.mikeboers.com/pyav/samples/' + name,
                           os.path.join('pyav-curated', name.replace('/', os.path.sep)))