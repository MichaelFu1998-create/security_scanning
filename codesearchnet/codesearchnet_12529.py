def paint(self):
        """
        Renders a javascript snippet suitable for use as a mapbox-gl fill-extrusion paint entry

        Returns:
            A dict that can be converted to a mapbox-gl javascript paint snippet
        """
        snippet = {
            'fill-extrusion-opacity': VectorStyle.get_style_value(self.opacity),
            'fill-extrusion-color': VectorStyle.get_style_value(self.color),
            'fill-extrusion-base': VectorStyle.get_style_value(self.base),
            'fill-extrusion-height': VectorStyle.get_style_value(self.height)
        }
        if self.translate:
            snippet['fill-extrusion-translate'] = self.translate

        return snippet