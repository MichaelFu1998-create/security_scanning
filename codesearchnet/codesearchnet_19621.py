def canny(img, threshold1=255/3, threshold2=255, **kwargs):
    """ canny edge """
    import cv2
    # edges=None, apertureSize=None, L2gradient=None
    if img.ndim <= 3:
        edge = cv2.Canny(img, threshold1, threshold2, **kwargs)
        if edge.ndim == 2:
            edge = np.expand_dims(edge, 2)
    elif img.ndim == 4:
        # batch
        edge = np.asarray([cv2.Canny(i, threshold1, threshold2, **kwargs) for i in img])
        if edge.ndim == 3:
            edge = np.expand_dims(edge, 3)
    else:
        raise ValueError('above 5d?')
    return edge