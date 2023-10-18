def write_output_metadata(output_params):
    """Dump output JSON and verify parameters if output metadata exist."""
    if "path" in output_params:
        metadata_path = os.path.join(output_params["path"], "metadata.json")
        logger.debug("check for output %s", metadata_path)
        try:
            existing_params = read_output_metadata(metadata_path)
            logger.debug("%s exists", metadata_path)
            logger.debug("existing output parameters: %s", pformat(existing_params))
            existing_tp = existing_params["pyramid"]
            current_params = params_to_dump(output_params)
            logger.debug("current output parameters: %s", pformat(current_params))
            current_tp = BufferedTilePyramid(**current_params["pyramid"])
            if existing_tp != current_tp:
                raise MapcheteConfigError(
                    "pyramid definitions between existing and new output do not match: "
                    "%s != %s" % (existing_tp, current_tp)
                )
            existing_format = existing_params["driver"]["format"]
            current_format = current_params["driver"]["format"]
            if existing_format != current_format:
                raise MapcheteConfigError(
                    "existing output format does not match new output format: "
                    "%s != %s" % (
                        (existing_format, current_format)
                    )
                )
        except FileNotFoundError:
            logger.debug("%s does not exist", metadata_path)
            dump_params = params_to_dump(output_params)
            # dump output metadata
            write_json(metadata_path, dump_params)
    else:
        logger.debug("no path parameter found")