def params_at_zoom(self, zoom):
        """
        Return configuration parameters snapshot for zoom as dictionary.

        Parameters
        ----------
        zoom : int
            zoom level

        Returns
        -------
        configuration snapshot : dictionary
        zoom level dependent process configuration
        """
        if zoom not in self.init_zoom_levels:
            raise ValueError(
                "zoom level not available with current configuration")
        out = dict(self._params_at_zoom[zoom], input={}, output=self.output)
        if "input" in self._params_at_zoom[zoom]:
            flat_inputs = {}
            for k, v in _flatten_tree(self._params_at_zoom[zoom]["input"]):
                if v is None:
                    flat_inputs[k] = None
                else:
                    flat_inputs[k] = self.input[get_hash(v)]
            out["input"] = _unflatten_tree(flat_inputs)
        else:
            out["input"] = {}
        return out