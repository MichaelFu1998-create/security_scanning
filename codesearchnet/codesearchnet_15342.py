def get_version_from_pc(search_dirs, target):
    """similar to 'pkg-config --modversion GraphicsMagick++'"""
    for dirname in search_dirs:
        for root, dirs, files in os.walk(dirname):
            for f in files:
                if f == target:
                    file_path = os.path.join(root, target)
                    _tmp = _grep("Version: ", file_path)
                    version = _tmp.split()[1]
                    print("Found version %s in file %s" % (version, file_path))
                    return version