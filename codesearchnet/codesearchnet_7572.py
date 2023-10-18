def check_md5sum_change(src_file):
    """Returns True if src_file has a different md5sum"""

    src_md5 = get_md5sum(src_file)

    src_md5_file = src_file + '.md5'
    src_file_changed = True
    if os.path.exists(src_md5_file):
        with open(src_md5_file, 'r') as file_checksum:
            ref_md5 = file_checksum.read()
        if src_md5 == ref_md5:
            src_file_changed = False

    if src_file_changed:
        with open(src_md5_file, 'w') as file_checksum:
            file_checksum.write(src_md5)

    return src_file_changed