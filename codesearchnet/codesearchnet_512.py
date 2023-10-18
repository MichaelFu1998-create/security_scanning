def load_cropped_svhn(path='data', include_extra=True):
    """Load Cropped SVHN.

    The Cropped Street View House Numbers (SVHN) Dataset contains 32x32x3 RGB images.
    Digit '1' has label 1, '9' has label 9 and '0' has label 0 (the original dataset uses 10 to represent '0'), see `ufldl website <http://ufldl.stanford.edu/housenumbers/>`__.

    Parameters
    ----------
    path : str
        The path that the data is downloaded to.
    include_extra : boolean
        If True (default), add extra images to the training set.

    Returns
    -------
    X_train, y_train, X_test, y_test: tuple
        Return splitted training/test set respectively.

    Examples
    ---------
    >>> X_train, y_train, X_test, y_test = tl.files.load_cropped_svhn(include_extra=False)
    >>> tl.vis.save_images(X_train[0:100], [10, 10], 'svhn.png')

    """
    start_time = time.time()

    path = os.path.join(path, 'cropped_svhn')
    logging.info("Load or Download Cropped SVHN > {} | include extra images: {}".format(path, include_extra))
    url = "http://ufldl.stanford.edu/housenumbers/"

    np_file = os.path.join(path, "train_32x32.npz")
    if file_exists(np_file) is False:
        filename = "train_32x32.mat"
        filepath = maybe_download_and_extract(filename, path, url)
        mat = sio.loadmat(filepath)
        X_train = mat['X'] / 255.0  # to [0, 1]
        X_train = np.transpose(X_train, (3, 0, 1, 2))
        y_train = np.squeeze(mat['y'], axis=1)
        y_train[y_train == 10] = 0  # replace 10 to 0
        np.savez(np_file, X=X_train, y=y_train)
        del_file(filepath)
    else:
        v = np.load(np_file)
        X_train = v['X']
        y_train = v['y']
    logging.info("  n_train: {}".format(len(y_train)))

    np_file = os.path.join(path, "test_32x32.npz")
    if file_exists(np_file) is False:
        filename = "test_32x32.mat"
        filepath = maybe_download_and_extract(filename, path, url)
        mat = sio.loadmat(filepath)
        X_test = mat['X'] / 255.0
        X_test = np.transpose(X_test, (3, 0, 1, 2))
        y_test = np.squeeze(mat['y'], axis=1)
        y_test[y_test == 10] = 0
        np.savez(np_file, X=X_test, y=y_test)
        del_file(filepath)
    else:
        v = np.load(np_file)
        X_test = v['X']
        y_test = v['y']
    logging.info("  n_test: {}".format(len(y_test)))

    if include_extra:
        logging.info("  getting extra 531131 images, please wait ...")
        np_file = os.path.join(path, "extra_32x32.npz")
        if file_exists(np_file) is False:
            logging.info("  the first time to load extra images will take long time to convert the file format ...")
            filename = "extra_32x32.mat"
            filepath = maybe_download_and_extract(filename, path, url)
            mat = sio.loadmat(filepath)
            X_extra = mat['X'] / 255.0
            X_extra = np.transpose(X_extra, (3, 0, 1, 2))
            y_extra = np.squeeze(mat['y'], axis=1)
            y_extra[y_extra == 10] = 0
            np.savez(np_file, X=X_extra, y=y_extra)
            del_file(filepath)
        else:
            v = np.load(np_file)
            X_extra = v['X']
            y_extra = v['y']
        # print(X_train.shape, X_extra.shape)
        logging.info("  adding n_extra {} to n_train {}".format(len(y_extra), len(y_train)))
        t = time.time()
        X_train = np.concatenate((X_train, X_extra), 0)
        y_train = np.concatenate((y_train, y_extra), 0)
        # X_train = np.append(X_train, X_extra, axis=0)
        # y_train = np.append(y_train, y_extra, axis=0)
        logging.info("  added n_extra {} to n_train {} took {}s".format(len(y_extra), len(y_train), time.time() - t))
    else:
        logging.info("  no extra images are included")
    logging.info("  image size: %s n_train: %d n_test: %d" % (str(X_train.shape[1:4]), len(y_train), len(y_test)))
    logging.info("  took: {}s".format(int(time.time() - start_time)))
    return X_train, y_train, X_test, y_test