def combine_filenames(filenames, max_length=40):
    """Return a new filename to use as the combined file name for a
    bunch of files, based on the SHA of their contents.
    A precondition is that they all have the same file extension

    Given that the list of files can have different paths, we aim to use the
    most common path.

    Example:
      /somewhere/else/foo.js
      /somewhere/bar.js
      /somewhere/different/too/foobar.js
    The result will be
      /somewhere/148713695b4a4b9083e506086f061f9c.js

    Another thing to note, if the filenames have timestamps in them, combine
    them all and use the highest timestamp.

    """
    # Get the SHA for each file, then sha all the shas.

    path = None
    names = []
    extension = None
    timestamps = []
    shas = []
    filenames.sort()
    concat_names = "_".join(filenames)
    if concat_names in COMBINED_FILENAMES_GENERATED:
        return COMBINED_FILENAMES_GENERATED[concat_names]

    for filename in filenames:
        name = os.path.basename(filename)
        if not extension:
            extension = os.path.splitext(name)[1]
        elif os.path.splitext(name)[1] != extension:
            raise ValueError("Can't combine multiple file extensions")

        for base in MEDIA_ROOTS:
            try:
                shas.append(md5(os.path.join(base, filename)))
                break
            except IOError:
                pass


        if path is None:
            path = os.path.dirname(filename)
        else:
            if len(os.path.dirname(filename)) < len(path):
                path = os.path.dirname(filename)

    m = hashlib.md5()
    m.update(",".join(shas))

    new_filename = "%s-inkmd" % m.hexdigest()

    new_filename = new_filename[:max_length]
    new_filename += extension
    COMBINED_FILENAMES_GENERATED[concat_names] = new_filename

    return os.path.join(path, new_filename)