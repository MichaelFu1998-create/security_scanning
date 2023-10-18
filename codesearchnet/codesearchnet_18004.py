def trisect_image(imshape, edgepts='calc'):
    """
    Returns 3 masks that trisect an image into 3 triangular portions.

    Parameters
    ----------
        imshape : 2-element list-like of ints
            The shape of the image. Elements after the first 2 are ignored.

        edgepts : Nested list-like, float, or `calc`, optional.
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

    Returns
    -------
        upper_mask : numpy.ndarray
            Boolean array; True in the image's upper  region.
        center_mask : numpy.ndarray
            Boolean array; True in the image's center region.
        lower_mask : numpy.ndarray
            Boolean array; True in the image's lower  region.
    """
    im_x, im_y = np.meshgrid(np.arange(imshape[0]), np.arange(imshape[1]),
            indexing='ij')
    if np.size(edgepts) == 1:
        #Gets equal-area sections, at sqrt(2/3) of the sides
        f = np.sqrt(2./3.) if edgepts == 'calc' else edgepts
        # f = np.sqrt(2./3.)
        lower_edge = (imshape[0] * (1-f),  imshape[1] * f)
        upper_edge = (imshape[0] * f,      imshape[1] * (1-f))
    else:
        upper_edge, lower_edge = edgepts

    #1. Get masks
    lower_slope = lower_edge[1] / max(float(imshape[0] - lower_edge[0]), 1e-9)
    upper_slope = (imshape[1] - upper_edge[1]) / float(upper_edge[0])
    #and the edge points are the x or y intercepts
    lower_intercept = -lower_slope * lower_edge[0]
    upper_intercept = upper_edge[1]
    lower_mask = im_y < (im_x * lower_slope + lower_intercept)
    upper_mask = im_y > (im_x * upper_slope + upper_intercept)

    center_mask= -(lower_mask | upper_mask)
    return upper_mask, center_mask, lower_mask