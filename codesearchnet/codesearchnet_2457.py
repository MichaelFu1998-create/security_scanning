def samples(dataset='imagenet', index=0, batchsize=1, shape=(224, 224),
            data_format='channels_last'):
    ''' Returns a batch of example images and the corresponding labels

    Parameters
    ----------
    dataset : string
        The data set to load (options: imagenet, mnist, cifar10,
        cifar100, fashionMNIST)
    index : int
        For each data set 20 example images exist. The returned batch
        contains the images with index [index, index + 1, index + 2, ...]
    batchsize : int
        Size of batch.
    shape : list of integers
        The shape of the returned image (only relevant for Imagenet).
    data_format : str
        "channels_first" or "channels_last"

    Returns
    -------
    images : array_like
        The batch of example images

    labels : array of int
        The labels associated with the images.

    '''
    from PIL import Image

    images, labels = [], []
    basepath = os.path.dirname(__file__)
    samplepath = os.path.join(basepath, 'data')
    files = os.listdir(samplepath)

    for idx in range(index, index + batchsize):
        i = idx % 20

        # get filename and label
        file = [n for n in files if '{}_{:02d}_'.format(dataset, i) in n][0]
        label = int(file.split('.')[0].split('_')[-1])

        # open file
        path = os.path.join(samplepath, file)
        image = Image.open(path)

        if dataset == 'imagenet':
            image = image.resize(shape)

        image = np.asarray(image, dtype=np.float32)

        if dataset != 'mnist' and data_format == 'channels_first':
            image = np.transpose(image, (2, 0, 1))

        images.append(image)
        labels.append(label)

    labels = np.array(labels)
    images = np.stack(images)
    return images, labels