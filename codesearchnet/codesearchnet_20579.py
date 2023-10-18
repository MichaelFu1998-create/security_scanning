def div_img(img1, div2):
    """ Pixelwise division or divide by a number """
    if is_img(div2):
        return img1.get_data()/div2.get_data()
    elif isinstance(div2, (float, int)):
        return img1.get_data()/div2
    else:
        raise NotImplementedError('Cannot divide {}({}) by '
                                  '{}({})'.format(type(img1),
                                                  img1,
                                                  type(div2),
                                                  div2))