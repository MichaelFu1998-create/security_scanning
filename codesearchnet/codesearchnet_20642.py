def insert_volumes_in_one_dataset(file_path, h5path, file_list, newshape=None,
                                  concat_axis=0, dtype=None, append=True):
    """Inserts all given nifti files from file_list into one dataset in fname.
    This will not check if the dimensionality of all files match.

    Parameters
    ----------
    file_path: string
        HDF5 file path

    h5path: string

    file_list: list of strings

    newshape: tuple or lambda function
        If None, it will not reshape the images.
        If a lambda function, this lambda will receive only the shape array.
        e.g., newshape = lambda x: (np.prod(x[0:3]), x[3])
        If a tuple, it will try to reshape all the images with the same shape.
        It must work for all the images in file_list.

    concat_axis: int
        Axis of concatenation after reshaping

    dtype: data type
    Dataset data type
    If not set, will use the type of the first file.

    append: bool

    Raises
    ------
    ValueError if concat_axis is bigger than data dimensionality.

    Note
    ----
    For now, this only works if the dataset ends up being a 2D matrix.
    I haven't tested for multi-dimensionality concatenations.
    """

    def isalambda(v):
        return isinstance(v, type(lambda: None)) and v.__name__ == '<lambda>'

    mode = 'w'
    if os.path.exists(file_path):
        if append:
            mode = 'a'

    #loading the metadata into spatialimages
    imgs = [nib.load(vol) for vol in file_list]

    #getting the shapes of all volumes
    shapes = [np.array(img.get_shape()) for img in imgs]

    #getting the reshaped shapes
    if newshape is not None:
        if isalambda(newshape):
            nushapes = np.array([newshape(shape) for shape in shapes])
        else:
            nushapes = np.array([shape for shape in shapes])

    #checking if concat_axis is available in this new shapes
    for nushape in nushapes:
        assert(len(nushape) - 1 < concat_axis)

    #calculate the shape of the new dataset
    n_dims = nushapes.shape[1]
    ds_shape = np.zeros(n_dims, dtype=np.int)
    for a in list(range(n_dims)):
        if a == concat_axis:
            ds_shape[a] = np.sum(nushapes[:, concat_axis])
        else:
            ds_shape[a] = np.max(nushapes[:, a])

    #get the type of the new dataset
    #dtypes = [img.get_data_dtype() for img in imgs]
    if dtype is None:
        dtype = imgs[0].get_data_dtype()

    with h5py.File(file_path, mode) as f:
        try:
            ic = 0
            h5grp = f.create_group(os.path.dirname(h5path))
            h5ds = h5grp.create_dataset(os.path.basename(h5path),
                                        ds_shape, dtype)
            for img in imgs:

                #get the shape of the current image
                nushape = nushapes[ic, :]

                def append_to_dataset(h5ds, idx, data, concat_axis):
                    """
                    @param h5ds: H5py DataSet
                    @param idx: int
                    @param data: ndarray
                    @param concat_axis: int
                    @return:
                    """
                    shape = data.shape
                    ndims = len(shape)

                    if ndims == 1:
                        if concat_axis == 0:
                            h5ds[idx] = data

                    elif ndims == 2:
                        if concat_axis == 0:
                            h5ds[idx ] = data
                        elif concat_axis == 1:
                            h5ds[idx ] = data

                    elif ndims == 3:
                        if concat_axis == 0:
                            h5ds[idx ] = data
                        elif concat_axis == 1:
                            h5ds[idx ] = data
                        elif concat_axis == 2:
                            h5ds[idx ] = data

                #appending the reshaped image into the dataset
                append_to_dataset(h5ds, ic,
                                  np.reshape(img.get_data(), tuple(nushape)),
                                  concat_axis)

                ic += 1

        except ValueError as ve:
            raise Exception('Error creating group {} in hdf file {}'.format(h5path, file_path)) from ve