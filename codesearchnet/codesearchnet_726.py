def class_balancing_oversample(X_train=None, y_train=None, printable=True):
    """Input the features and labels, return the features and labels after oversampling.

    Parameters
    ----------
    X_train : numpy.array
        The inputs.
    y_train : numpy.array
        The targets.

    Examples
    --------
    One X

    >>> X_train, y_train = class_balancing_oversample(X_train, y_train, printable=True)

    Two X

    >>> X, y = tl.utils.class_balancing_oversample(X_train=np.hstack((X1, X2)), y_train=y, printable=False)
    >>> X1 = X[:, 0:5]
    >>> X2 = X[:, 5:]

    """
    # ======== Classes balancing
    if printable:
        tl.logging.info("Classes balancing for training examples...")

    c = Counter(y_train)

    if printable:
        tl.logging.info('the occurrence number of each stage: %s' % c.most_common())
        tl.logging.info('the least stage is Label %s have %s instances' % c.most_common()[-1])
        tl.logging.info('the most stage is  Label %s have %s instances' % c.most_common(1)[0])

    most_num = c.most_common(1)[0][1]

    if printable:
        tl.logging.info('most num is %d, all classes tend to be this num' % most_num)

    locations = {}
    number = {}

    for lab, num in c.most_common():  # find the index from y_train
        number[lab] = num
        locations[lab] = np.where(np.array(y_train) == lab)[0]
    if printable:
        tl.logging.info('convert list(np.array) to dict format')
    X = {}  # convert list to dict
    for lab, num in number.items():
        X[lab] = X_train[locations[lab]]

    # oversampling
    if printable:
        tl.logging.info('start oversampling')
    for key in X:
        temp = X[key]
        while True:
            if len(X[key]) >= most_num:
                break
            X[key] = np.vstack((X[key], temp))
    if printable:
        tl.logging.info('first features of label 0 > %d' % len(X[0][0]))
        tl.logging.info('the occurrence num of each stage after oversampling')
    for key in X:
        tl.logging.info("%s %d" % (key, len(X[key])))
    if printable:
        tl.logging.info('make each stage have same num of instances')
    for key in X:
        X[key] = X[key][0:most_num, :]
        tl.logging.info("%s %d" % (key, len(X[key])))

    # convert dict to list
    if printable:
        tl.logging.info('convert from dict to list format')
    y_train = []
    X_train = np.empty(shape=(0, len(X[0][0])))
    for key in X:
        X_train = np.vstack((X_train, X[key]))
        y_train.extend([key for i in range(len(X[key]))])
    # tl.logging.info(len(X_train), len(y_train))
    c = Counter(y_train)
    if printable:
        tl.logging.info('the occurrence number of each stage after oversampling: %s' % c.most_common())
    # ================ End of Classes balancing
    return X_train, y_train