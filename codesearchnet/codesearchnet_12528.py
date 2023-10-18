def paint(self):
        """
        Renders a javascript snippet suitable for use as a mapbox-gl fill paint entry

        Returns:
            A dict that can be converted to a mapbox-gl javascript paint snippet
        """
        snippet = {
            'fill-opacity': VectorStyle.get_style_value(self.opacity),
            'fill-color': VectorStyle.get_style_value(self.color),
            'fill-outline-color': VectorStyle.get_style_value(self.outline_color)
        }
        if self.translate:
            snippet['fill-translate'] = self.translate

        return snippet