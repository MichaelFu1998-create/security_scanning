def _read_config_file(config_file, verbose):
    """Read configuration file options into a dictionary."""

    config_file = os.path.abspath(config_file)

    if not os.path.exists(config_file):
        raise RuntimeError("Couldn't open configuration file '{}'.".format(config_file))

    if config_file.endswith(".json"):
        with io.open(config_file, mode="r", encoding="utf-8") as json_file:
            # Minify the JSON file to strip embedded comments
            minified = jsmin(json_file.read())
        conf = json.loads(minified)

    elif config_file.endswith(".yaml"):
        with io.open(config_file, mode="r", encoding="utf-8") as yaml_file:
            conf = yaml.safe_load(yaml_file)

    else:
        try:
            import imp

            conf = {}
            configmodule = imp.load_source("configuration_module", config_file)

            for k, v in vars(configmodule).items():
                if k.startswith("__"):
                    continue
                elif isfunction(v):
                    continue
                conf[k] = v
        except Exception:
            exc_type, exc_value = sys.exc_info()[:2]
            exc_info_list = traceback.format_exception_only(exc_type, exc_value)
            exc_text = "\n".join(exc_info_list)
            print(
                "Failed to read configuration file: "
                + config_file
                + "\nDue to "
                + exc_text,
                file=sys.stderr,
            )
            raise

    conf["_config_file"] = config_file
    return conf