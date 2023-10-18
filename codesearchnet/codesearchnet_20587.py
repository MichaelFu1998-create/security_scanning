def write_meta_header(filename, meta_dict):
    """ Write the content of the `meta_dict` into `filename`.

    Parameters
    ----------
    filename: str
        Path to the output file

    meta_dict: dict
        Dictionary with the fields of the metadata .mhd file
    """
    header = ''
    # do not use tags = meta_dict.keys() because the order of tags matters
    for tag in MHD_TAGS:
        if tag in meta_dict.keys():
            header += '{} = {}\n'.format(tag, meta_dict[tag])

    with open(filename, 'w') as f:
        f.write(header)