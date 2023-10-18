def paint(self):
        """
        Renders a javascript snippet suitable for use as a mapbox-gl line paint entry

        Returns:
            A dict that can be converted to a mapbox-gl javascript paint snippet
        """
        # TODO Figure out why i cant use some of these props
        snippet = {
            'line-opacity': VectorStyle.get_style_value(self.opacity),
            'line-color': VectorStyle.get_style_value(self.color),
            #'line-cap': self.cap,
            #'line-join': self.join,
            'line-width': VectorStyle.get_style_value(self.width),
            #'line-gap-width': self.gap_width,
            #'line-blur': self.blur,
        }
        if self.translate:
            snippet['line-translate'] = self.translate

        if self.dasharray:
            snippet['line-dasharray'] = VectorStyle.get_style_value(self.dasharray)

        return snippet