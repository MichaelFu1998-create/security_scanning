def layers(self):
        """ Renders the list of layers to add to the map.

            Returns:
                layers (list): list of layer entries suitable for use in mapbox-gl 'map.addLayer()' call
        """
        layers = [self._layer_def(style) for style in self.styles]
        return layers