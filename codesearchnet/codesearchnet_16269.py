def write_shas_to_shastore(sha_dict):
    """
    Writes a sha1 dictionary stored in memory to
    the .shastore file
    """
    if sys.version_info[0] < 3:
        fn_open = open
    else:
        fn_open = io.open
    with fn_open(".shastore", "w") as fh:
        fh.write("---\n")
        fh.write('sake version: {}\n'.format(constants.VERSION))
        if sha_dict:
            fh.write(yaml.dump(sha_dict))
        fh.write("...")