def _get_layer(self, layer_id):
        """
        :return: the layer with the :paramref:`layer_id`. If the layer
          does not exist, it is created.
        :param str layer_id: the id of the layer
        """
        if layer_id not in self._layer_id_to_layer:
            self._svg.setdefault("g", [])
            layer = {
                "g": [],
                "@inkscape:label": layer_id,
                "@id": layer_id,
                "@inkscape:groupmode": "layer",
                "@class": "row"
            }
            self._layer_id_to_layer[layer_id] = layer
            self._svg["g"].append(layer)
        return self._layer_id_to_layer[layer_id]