def fate(name):
    """Download and return a path to a sample from the FFmpeg test suite.

    Data is handled by :func:`cached_download`.

    See the `FFmpeg Automated Test Environment <https://www.ffmpeg.org/fate.html>`_

    """
    return cached_download('http://fate.ffmpeg.org/fate-suite/' + name,
                           os.path.join('fate-suite', name.replace('/', os.path.sep)))