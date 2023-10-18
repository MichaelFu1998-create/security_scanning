def create_archive(directory, filename, config={}, ignore_predicate=None, ignored_files=['.git', '.svn']):
    """
    Creates an archive from a directory and returns
    the file that was created.
    """
    with zipfile.ZipFile(filename, 'w', compression=zipfile.ZIP_DEFLATED) as zip_file:
        root_len = len(os.path.abspath(directory))

        # create it
        out("Creating archive: " + str(filename))
        for root, dirs, files in os.walk(directory, followlinks=True):
            archive_root = os.path.abspath(root)[root_len + 1:]
            for f in files:
                fullpath = os.path.join(root, f)
                archive_name = os.path.join(archive_root, f)

                # ignore the file we're creating
                if filename in fullpath:
                    continue

                # ignored files
                if ignored_files is not None:
                    for name in ignored_files:
                        if fullpath.endswith(name):
                            out("Skipping: " + str(name))
                            continue

                # do predicate
                if ignore_predicate is not None:
                    if not ignore_predicate(archive_name):
                        out("Skipping: " + str(archive_name))
                        continue

                out("Adding: " + str(archive_name))
                zip_file.write(fullpath, archive_name, zipfile.ZIP_DEFLATED)

    return filename