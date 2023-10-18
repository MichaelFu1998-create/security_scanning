def unzip(zipped_file, output_directory=None,
          prefix="harvestingkit_unzip_", suffix=""):
    """Uncompress a zipped file from given filepath to an (optional) location.

    If no location is given, a temporary folder will be generated inside
    CFG_TMPDIR, prefixed with "apsharvest_unzip_".
    """
    if not output_directory:
        # We create a temporary directory to extract our stuff in
        try:
            output_directory = mkdtemp(suffix=suffix,
                                       prefix=prefix)
        except Exception, e:
            try:
                os.removedirs(output_directory)
            except TypeError:
                pass
            raise e
    return _do_unzip(zipped_file, output_directory)