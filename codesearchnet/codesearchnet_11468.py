def compile_masks(masks):
    """
    Compiles a list of regular expressions.

    :param masks: the regular expressions to compile
    :type masks: list(str) or str
    :returns: list(regular expression object)
    """

    if not masks:
        masks = []
    elif not isinstance(masks, (list, tuple)):
        masks = [masks]

    return [
        re.compile(mask)
        for mask in masks
    ]