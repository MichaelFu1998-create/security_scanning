def read_labels(filename, delimiter=DEFAULT_DELIMITER):
    """read label files. Format: ent label"""
    _assert_good_file(filename)
    with open(filename) as f:
        labels = [_label_processing(l, delimiter) for l in f]
        return labels