def rand_rotate(anglerange, *imagez):
    """
    :param anglerange:
    :param imagez:
    :return:
    """
    r = float(anglerange[1] - anglerange[0])
    s = anglerange[0]

    def _rand_rotate(*imgz):
        angle = np.random.random(1)[0] * r + s
        out = tuple(rotate(img, angle) for img in imgz)
        return tuple_or_not(out)

    return _rand_rotate(*imagez) if imagez else _rand_rotate