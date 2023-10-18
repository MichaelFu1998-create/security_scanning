def parse_darknet_ann_str_to_list(annotations):
    r"""Input string format of class, x, y, w, h, return list of list format.

    Parameters
    -----------
    annotations : str
        The annotations in darkent format "class, x, y, w, h ...." seperated by "\\n".

    Returns
    -------
    list of list of 4 numbers
        List of bounding box.

    """
    annotations = annotations.split("\n")
    ann = []
    for a in annotations:
        a = a.split()
        if len(a) == 5:
            for i, _v in enumerate(a):
                if i == 0:
                    a[i] = int(a[i])
                else:
                    a[i] = float(a[i])
            ann.append(a)
    return ann