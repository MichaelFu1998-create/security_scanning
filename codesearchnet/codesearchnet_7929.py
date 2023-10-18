def remove_binaries():
    """Remove all binary files in the adslib directory."""
    patterns = (
        "adslib/*.a",
        "adslib/*.o",
        "adslib/obj/*.o",
        "adslib/*.bin",
        "adslib/*.so",
    )

    for f in functools.reduce(operator.iconcat, [glob.glob(p) for p in patterns]):
        os.remove(f)