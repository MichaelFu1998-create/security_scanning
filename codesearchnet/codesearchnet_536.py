def natural_keys(text):
    """Sort list of string with number in human order.

    Examples
    ----------
    >>> l = ['im1.jpg', 'im31.jpg', 'im11.jpg', 'im21.jpg', 'im03.jpg', 'im05.jpg']
    >>> l.sort(key=tl.files.natural_keys)
    ['im1.jpg', 'im03.jpg', 'im05', 'im11.jpg', 'im21.jpg', 'im31.jpg']
    >>> l.sort() # that is what we dont want
    ['im03.jpg', 'im05', 'im1.jpg', 'im11.jpg', 'im21.jpg', 'im31.jpg']

    References
    ----------
    - `link <http://nedbatchelder.com/blog/200712/human_sorting.html>`__

    """

    # - alist.sort(key=natural_keys) sorts in human order
    # http://nedbatchelder.com/blog/200712/human_sorting.html
    # (See Toothy's implementation in the comments)
    def atoi(text):
        return int(text) if text.isdigit() else text

    return [atoi(c) for c in re.split('(\d+)', text)]