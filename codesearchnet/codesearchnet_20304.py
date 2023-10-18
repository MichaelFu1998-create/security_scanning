def compress(images, delete_tif=False, folder=None):
    """Lossless compression. Save images as PNG and TIFF tags to json. Can be
    reversed with `decompress`. Will run in multiprocessing, where
    number of workers is decided by ``leicaexperiment.experiment._pools``.

    Parameters
    ----------
    images : list of filenames
        Images to lossless compress.
    delete_tif : bool
        Wheter to delete original images.
    folder : string
        Where to store images. Basename will be kept.

    Returns
    -------
    list of filenames
        List of compressed files.
    """
    if type(images) == str:
        # only one image
        return [compress_blocking(images, delete_tif, folder)]

    filenames = copy(images) # as images property will change when looping


    return Parallel(n_jobs=_pools)(delayed(compress_blocking)
                     (image=image, delete_tif=delete_tif, folder=folder)
                     for image in filenames)