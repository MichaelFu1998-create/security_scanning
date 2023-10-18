def get_md5sum(src_file):
    """Returns md5sum of file"""

    with open(src_file, 'r') as src_data:
        src_content = src_data.read()

        # data needs to be encoded in python3 before hashing
        if sys.version_info[0] == 3:
            src_content = src_content.encode('utf-8')

        src_md5 = hashlib.md5(src_content).hexdigest()
    return src_md5