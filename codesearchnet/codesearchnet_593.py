def parse_darknet_ann_list_to_cls_box(annotations):
    """Parse darknet annotation format into two lists for class and bounding box.

    Input list of [[class, x, y, w, h], ...], return two list of [class ...] and [[x, y, w, h], ...].

    Parameters
    ------------
    annotations : list of list
        A list of class and bounding boxes of images e.g. [[class, x, y, w, h], ...]

    Returns
    -------
    list of int
        List of class labels.

    list of list of 4 numbers
        List of bounding box.

    """
    class_list = []
    bbox_list = []
    for ann in annotations:
        class_list.append(ann[0])
        bbox_list.append(ann[1:])
    return class_list, bbox_list