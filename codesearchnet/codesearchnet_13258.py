def multi_segment(annotation, sr=22050, length=None, **kwargs):
    '''Sonify multi-level segmentations'''

    # Pentatonic scale, because why not
    PENT = [1, 32./27, 4./3, 3./2, 16./9]
    DURATION = 0.1

    h_int, _ = hierarchy_flatten(annotation)

    if length is None:
        length = int(sr * (max(np.max(_) for _ in h_int) + 1. / DURATION) + 1)

    y = 0.0
    for ints, (oc, scale) in zip(h_int, product(range(3, 3 + len(h_int)),
                                                PENT)):
        click = mkclick(440.0 * scale * oc, sr=sr, duration=DURATION)
        y = y + filter_kwargs(mir_eval.sonify.clicks,
                              np.unique(ints),
                              fs=sr, length=length,
                              click=click)
    return y