def paint(self):
        """
        Renders a javascript snippet suitable for use as a mapbox-gl heatmap paint entry

        Returns:
            A dict that can be converted to a mapbox-gl javascript paint snippet
        """
        snippet = {
            'heatmap-radius': VectorStyle.get_style_value(self.radius),
            'heatmap-opacity': VectorStyle.get_style_value(self.opacity),
            'heatmap-color': VectorStyle.get_style_value(self.color),
            'heatmap-intensity': VectorStyle.get_style_value(self.intensity),
            'heatmap-weight': VectorStyle.get_style_value(self.weight)
        }

        return snippet