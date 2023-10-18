def check_shastore_version(from_store, settings):
    """
    This function gives us the option to emit errors or warnings
    after sake upgrades
    """
    sprint = settings["sprint"]
    error = settings["error"]

    sprint("checking .shastore version for potential incompatibilities",
           level="verbose")
    if not from_store or 'sake version' not in from_store:
        errmes = ["Since you've used this project last, a new version of ",
                  "sake was installed that introduced backwards incompatible",
                  " changes. Run 'sake clean', and rebuild before continuing\n"]
        errmes = " ".join(errmes)
        error(errmes)
        sys.exit(1)