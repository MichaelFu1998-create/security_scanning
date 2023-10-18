def threading_data(data=None, fn=None, thread_count=None, **kwargs):
    """Process a batch of data by given function by threading.

    Usually be used for data augmentation.

    Parameters
    -----------
    data : numpy.array or others
        The data to be processed.
    thread_count : int
        The number of threads to use.
    fn : function
        The function for data processing.
    more args : the args for `fn`
        Ssee Examples below.

    Examples
    --------
    Process images.

    >>> images, _, _, _ = tl.files.load_cifar10_dataset(shape=(-1, 32, 32, 3))
    >>> images = tl.prepro.threading_data(images[0:32], tl.prepro.zoom, zoom_range=[0.5, 1])

    Customized image preprocessing function.

    >>> def distort_img(x):
    >>>     x = tl.prepro.flip_axis(x, axis=0, is_random=True)
    >>>     x = tl.prepro.flip_axis(x, axis=1, is_random=True)
    >>>     x = tl.prepro.crop(x, 100, 100, is_random=True)
    >>>     return x
    >>> images = tl.prepro.threading_data(images, distort_img)

    Process images and masks together (Usually be used for image segmentation).

    >>> X, Y --> [batch_size, row, col, 1]
    >>> data = tl.prepro.threading_data([_ for _ in zip(X, Y)], tl.prepro.zoom_multi, zoom_range=[0.5, 1], is_random=True)
    data --> [batch_size, 2, row, col, 1]
    >>> X_, Y_ = data.transpose((1,0,2,3,4))
    X_, Y_ --> [batch_size, row, col, 1]
    >>> tl.vis.save_image(X_, 'images.png')
    >>> tl.vis.save_image(Y_, 'masks.png')

    Process images and masks together by using ``thread_count``.

    >>> X, Y --> [batch_size, row, col, 1]
    >>> data = tl.prepro.threading_data(X, tl.prepro.zoom_multi, 8, zoom_range=[0.5, 1], is_random=True)
    data --> [batch_size, 2, row, col, 1]
    >>> X_, Y_ = data.transpose((1,0,2,3,4))
    X_, Y_ --> [batch_size, row, col, 1]
    >>> tl.vis.save_image(X_, 'after.png')
    >>> tl.vis.save_image(Y_, 'before.png')

    Customized function for processing images and masks together.

    >>> def distort_img(data):
    >>>    x, y = data
    >>>    x, y = tl.prepro.flip_axis_multi([x, y], axis=0, is_random=True)
    >>>    x, y = tl.prepro.flip_axis_multi([x, y], axis=1, is_random=True)
    >>>    x, y = tl.prepro.crop_multi([x, y], 100, 100, is_random=True)
    >>>    return x, y

    >>> X, Y --> [batch_size, row, col, channel]
    >>> data = tl.prepro.threading_data([_ for _ in zip(X, Y)], distort_img)
    >>> X_, Y_ = data.transpose((1,0,2,3,4))

    Returns
    -------
    list or numpyarray
        The processed results.

    References
    ----------
    - `python queue <https://pymotw.com/2/Queue/index.html#module-Queue>`__
    - `run with limited queue <http://effbot.org/librarybook/queue.htm>`__

    """

    def apply_fn(results, i, data, kwargs):
        results[i] = fn(data, **kwargs)

    if thread_count is None:
        results = [None] * len(data)
        threads = []
        # for i in range(len(data)):
        #     t = threading.Thread(name='threading_and_return', target=apply_fn, args=(results, i, data[i], kwargs))
        for i, d in enumerate(data):
            t = threading.Thread(name='threading_and_return', target=apply_fn, args=(results, i, d, kwargs))
            t.start()
            threads.append(t)
    else:
        divs = np.linspace(0, len(data), thread_count + 1)
        divs = np.round(divs).astype(int)
        results = [None] * thread_count
        threads = []
        for i in range(thread_count):
            t = threading.Thread(
                name='threading_and_return', target=apply_fn, args=(results, i, data[divs[i]:divs[i + 1]], kwargs)
            )
            t.start()
            threads.append(t)

    for t in threads:
        t.join()

    if thread_count is None:
        try:
            return np.asarray(results)
        except Exception:
            return results
    else:
        return np.concatenate(results)