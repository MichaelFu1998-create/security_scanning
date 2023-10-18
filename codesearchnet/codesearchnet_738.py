def read_words(filename="nietzsche.txt", replace=None):
    """Read list format context from a file.

    For customized read_words method, see ``tutorial_generate_text.py``.

    Parameters
    ----------
    filename : str
        a file path.
    replace : list of str
        replace original string by target string.

    Returns
    -------
    list of str
        The context in a list (split using space).
    """
    if replace is None:
        replace = ['\n', '<eos>']

    with tf.gfile.GFile(filename, "r") as f:
        try:  # python 3.4 or older
            context_list = f.read().replace(*replace).split()
        except Exception:  # python 3.5
            f.seek(0)
            replace = [x.encode('utf-8') for x in replace]
            context_list = f.read().replace(*replace).split()
        return context_list