def write_main(argv):
    """
    write FILENAME
        Write a local copy of FILENAME using FILENAME_tweaks for local tweaks.
    """
    if len(argv) != 1:
        print("Please provide the name of a file to write.")
        return 1

    filename = argv[0]
    resource_name = "files/" + filename
    tweaks_name = amend_filename(filename, "_tweaks")

    if not pkg_resources.resource_exists("edx_lint", resource_name):
        print(u"Don't have file %r to write." % filename)
        return 2

    if os.path.exists(filename):
        print(u"Checking existing copy of %s" % filename)
        tef = TamperEvidentFile(filename)
        if not tef.validate():
            bak_name = amend_filename(filename, "_backup")
            print(u"Your copy of %s seems to have been edited, renaming it to %s" % (filename, bak_name))
            if os.path.exists(bak_name):
                print(u"A previous %s exists, deleting it" % bak_name)
                os.remove(bak_name)
            os.rename(filename, bak_name)

    print(u"Reading edx_lint/files/%s" % filename)
    cfg = configparser.RawConfigParser()
    resource_string = pkg_resources.resource_string("edx_lint", resource_name).decode("utf8")

    # pkg_resources always reads binary data (in both python2 and python3).
    # ConfigParser.read_string only exists in python3, so we have to wrap the string
    # from pkg_resources in a cStringIO so that we can pass it into ConfigParser.readfp.
    if six.PY2:
        cfg.readfp(cStringIO(resource_string), resource_name)
    else:
        cfg.read_string(resource_string, resource_name)     # pylint: disable=no-member

    if os.path.exists(tweaks_name):
        print(u"Applying local tweaks from %s" % tweaks_name)
        cfg_tweaks = configparser.RawConfigParser()
        cfg_tweaks.read([tweaks_name])

        merge_configs(cfg, cfg_tweaks)

    print(u"Writing %s" % filename)
    output_text = cStringIO()
    output_text.write(WARNING_HEADER.format(filename=filename, tweaks_name=tweaks_name))
    cfg.write(output_text)

    out_tef = TamperEvidentFile(filename)
    if six.PY2:
        output_bytes = output_text.getvalue()
    else:
        output_bytes = output_text.getvalue().encode("utf8")
    out_tef.write(output_bytes)

    return 0