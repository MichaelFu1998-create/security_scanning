def set_meta(target, keys, overwrite=False):
    """Write metadata keys to .md file.

    TARGET can be a media file or an album directory. KEYS are key/value pairs.

    Ex, to set the title of test.jpg to "My test image":

    sigal set_meta test.jpg title "My test image"
    """

    if not os.path.exists(target):
        sys.stderr.write("The target {} does not exist.\n".format(target))
        sys.exit(1)
    if len(keys) < 2 or len(keys) % 2 > 0:
        sys.stderr.write("Need an even number of arguments.\n")
        sys.exit(1)

    if os.path.isdir(target):
        descfile = os.path.join(target, 'index.md')
    else:
        descfile = os.path.splitext(target)[0] + '.md'
    if os.path.exists(descfile) and not overwrite:
        sys.stderr.write("Description file '{}' already exists. "
                         "Use --overwrite to overwrite it.\n".format(descfile))
        sys.exit(2)

    with open(descfile, "w") as fp:
        for i in range(len(keys) // 2):
            k, v = keys[i * 2:(i + 1) * 2]
            fp.write("{}: {}\n".format(k.capitalize(), v))
    print("{} metadata key(s) written to {}".format(len(keys) // 2, descfile))