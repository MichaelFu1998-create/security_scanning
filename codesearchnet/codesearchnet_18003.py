def compare_data_model_residuals(s, tile, data_vmin='calc', data_vmax='calc',
         res_vmin=-0.1, res_vmax=0.1, edgepts='calc', do_imshow=True,
         data_cmap=plt.cm.bone, res_cmap=plt.cm.RdBu):
    """
    Compare the data, model, and residuals of a state.

    Makes an image of any 2D slice of a state that compares the data,
    model, and residuals. The upper left portion of the image is the raw
    data, the central portion the model, and the lower right portion the
    image. Either plots the image using plt.imshow() or returns a
    np.ndarray of the image pixels for later use.

    Parameters
    ----------
        st : peri.ImageState object
            The state to plot.
        tile : peri.util.Tile object
            The slice of the image to plot. Can be any xy, xz, or yz
            projection, but it must return a valid 2D slice (the slice is
            squeezed internally).

        data_vmin : {Float, `calc`}, optional
            vmin for the imshow for the data and generative model (shared).
            Default is 'calc' = 0.5(data.min() + model.min())
        data_vmax : {Float, `calc`}, optional
            vmax for the imshow for the data and generative model (shared).
            Default is 'calc' = 0.5(data.max() + model.max())
        res_vmin : Float, optional
            vmin for the imshow for the residuals. Default is -0.1
            Default is 'calc' = 0.5(data.min() + model.min())
        res_vmax : Float, optional
            vmax for the imshow for the residuals. Default is +0.1
        edgepts : {Nested list-like, Float, 'calc'}, optional.
            The vertices of the triangles which determine the splitting of
            the image. The vertices are at (image corner, (edge, y), and
            (x,edge), where edge is the appropriate edge of the image.
                edgepts[0] : (x,y) points for the upper edge
                edgepts[1] : (x,y) points for the lower edge
            where `x` is the coordinate along the image's 0th axis and `y`
            along the images 1st axis. Default is 'calc,' which calculates
            edge points by splitting the image into 3 regions of equal
            area. If edgepts is a float scalar, calculates the edge points
            based on a constant fraction of distance from the edge.
        do_imshow : Bool
            If True, imshow's and returns the returned handle.
            If False, returns the array as a [M,N,4] array.
        data_cmap : matplotlib colormap instance
            The colormap to use for the data and model.
        res_cmap : matplotlib colormap instance
            The colormap to use for the residuals.

    Returns
    -------
        image : {matplotlib.pyplot.AxesImage, numpy.ndarray}
            If `do_imshow` == True, the returned handle from imshow.
            If `do_imshow` == False, an [M,N,4] np.ndarray of the image
            pixels.
    """
    # This could be modified to alpha the borderline... or to embiggen
    # the image and slice it more finely
    residuals = s.residuals[tile.slicer].squeeze()
    data = s.data[tile.slicer].squeeze()
    model = s.model[tile.slicer].squeeze()
    if data.ndim != 2:
        raise ValueError('tile does not give a 2D slice')

    im = np.zeros([data.shape[0], data.shape[1], 4])
    if data_vmin == 'calc':
        data_vmin = 0.5*(data.min() + model.min())
    if data_vmax == 'calc':
        data_vmax = 0.5*(data.max() + model.max())

    #1. Get masks:
    upper_mask, center_mask, lower_mask = trisect_image(im.shape, edgepts)

    #2. Get colorbar'd images
    gm = data_cmap(center_data(model, data_vmin, data_vmax))
    dt = data_cmap(center_data(data, data_vmin, data_vmax))
    rs = res_cmap(center_data(residuals, res_vmin, res_vmax))

    for a in range(4):
        im[:,:,a][upper_mask] = rs[:,:,a][upper_mask]
        im[:,:,a][center_mask] = gm[:,:,a][center_mask]
        im[:,:,a][lower_mask] = dt[:,:,a][lower_mask]
    if do_imshow:
        return plt.imshow(im)
    else:
        return im