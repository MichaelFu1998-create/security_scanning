def _read_meta_header(filename):
    """Return a dictionary of meta data from meta header file.

    Parameters
    ----------
    filename: str
        Path to a .mhd file

    Returns
    -------
    meta_dict: dict
        A dictionary with the .mhd header content.
    """
    fileIN = open(filename, 'r')
    line   = fileIN.readline()

    meta_dict = {}
    tag_flag = [False]*len(MHD_TAGS)
    while line:
        tags = str.split(line, '=')
        # print tags[0]
        for i in range(len(MHD_TAGS)):
            tag = MHD_TAGS[i]
            if (str.strip(tags[0]) == tag) and (not tag_flag[i]):
                # print tags[1]
                meta_dict[tag] = str.strip(tags[1])
                tag_flag[i] = True
        line = fileIN.readline()
    #  comment
    fileIN.close()
    return meta_dict