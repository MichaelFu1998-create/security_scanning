def repr_imgs(imgs):
    """Printing of img or imgs"""
    if isinstance(imgs, string_types):
        return imgs

    if isinstance(imgs, collections.Iterable):
        return '[{}]'.format(', '.join(repr_imgs(img) for img in imgs))

    # try get_filename
    try:
        filename = imgs.get_filename()
        if filename is not None:
            img_str = "{}('{}')".format(imgs.__class__.__name__, filename)
        else:
            img_str = "{}(shape={}, affine={})".format(imgs.__class__.__name__,
                                                       repr(get_shape(imgs)),
                                                       repr(imgs.get_affine()))
    except Exception as exc:
        log.error('Error reading attributes from img.get_filename()')
        return repr(imgs)
    else:
        return img_str