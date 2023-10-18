def output(self):
        """Output object of driver."""
        output_params = dict(
            self._raw["output"],
            grid=self.output_pyramid.grid,
            pixelbuffer=self.output_pyramid.pixelbuffer,
            metatiling=self.output_pyramid.metatiling
        )
        if "path" in output_params:
            output_params.update(
                path=absolute_path(path=output_params["path"], base_dir=self.config_dir)
            )

        if "format" not in output_params:
            raise MapcheteConfigError("output format not specified")

        if output_params["format"] not in available_output_formats():
            raise MapcheteConfigError(
                "format %s not available in %s" % (
                    output_params["format"], str(available_output_formats())
                )
            )
        writer = load_output_writer(output_params)
        try:
            writer.is_valid_with_config(output_params)
        except Exception as e:
            logger.exception(e)
            raise MapcheteConfigError(
                "driver %s not compatible with configuration: %s" % (
                    writer.METADATA["driver_name"], e
                )
            )
        return writer