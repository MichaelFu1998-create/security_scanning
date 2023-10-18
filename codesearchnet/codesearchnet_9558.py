def input(self):
        """
        Input items used for process stored in a dictionary.

        Keys are the hashes of the input parameters, values the respective
        InputData classes.
        """
        # the delimiters are used by some input drivers
        delimiters = dict(
            zoom=self.init_zoom_levels,
            bounds=self.init_bounds,
            process_bounds=self.bounds,
            effective_bounds=self.effective_bounds
        )

        # get input items only of initialized zoom levels
        raw_inputs = {
            # convert input definition to hash
            get_hash(v): v
            for zoom in self.init_zoom_levels
            if "input" in self._params_at_zoom[zoom]
            # to preserve file groups, "flatten" the input tree and use
            # the tree paths as keys
            for key, v in _flatten_tree(self._params_at_zoom[zoom]["input"])
            if v is not None
        }

        initalized_inputs = {}
        for k, v in raw_inputs.items():

            # for files and tile directories
            if isinstance(v, str):
                logger.debug("load input reader for simple input %s",  v)
                try:
                    reader = load_input_reader(
                        dict(
                            path=absolute_path(path=v, base_dir=self.config_dir),
                            pyramid=self.process_pyramid,
                            pixelbuffer=self.process_pyramid.pixelbuffer,
                            delimiters=delimiters
                        ),
                        readonly=self.mode == "readonly")
                except Exception as e:
                    logger.exception(e)
                    raise MapcheteDriverError("error when loading input %s: %s" % (v, e))
                logger.debug("input reader for simple input %s is %s", v, reader)

            # for abstract inputs
            elif isinstance(v, dict):
                logger.debug("load input reader for abstract input %s", v)
                try:
                    reader = load_input_reader(
                        dict(
                            abstract=deepcopy(v),
                            pyramid=self.process_pyramid,
                            pixelbuffer=self.process_pyramid.pixelbuffer,
                            delimiters=delimiters,
                            conf_dir=self.config_dir
                        ),
                        readonly=self.mode == "readonly")
                except Exception as e:
                    logger.exception(e)
                    raise MapcheteDriverError("error when loading input %s: %s" % (v, e))
                logger.debug("input reader for abstract input %s is %s", v, reader)
            else:
                raise MapcheteConfigError("invalid input type %s", type(v))
            # trigger bbox creation
            reader.bbox(out_crs=self.process_pyramid.crs)
            initalized_inputs[k] = reader

        return initalized_inputs