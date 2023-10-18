def read_images(img_list, path='', n_threads=10, printable=True):
    """Returns all images in list by given path and name of each image file.

    Parameters
    -------------
    img_list : list of str
        The image file names.
    path : str
        The image folder path.
    n_threads : int
        The number of threads to read image.
    printable : boolean
        Whether to print information when reading images.

    Returns
    -------
    list of numpy.array
        The images.

    """
    imgs = []
    for idx in range(0, len(img_list), n_threads):
        b_imgs_list = img_list[idx:idx + n_threads]
        b_imgs = tl.prepro.threading_data(b_imgs_list, fn=read_image, path=path)
        # tl.logging.info(b_imgs.shape)
        imgs.extend(b_imgs)
        if printable:
            tl.logging.info('read %d from %s' % (len(imgs), path))
    return imgs