def place(self, x, y, svg, layer_id):
        """Place the :paramref:`svg` content at ``(x, y)`` position
        in the SVG, in a layer with the id :paramref:`layer_id`.

        :param float x: the x position of the svg
        :param float y: the y position of the svg
        :param str svg: the SVG to place at ``(x, y)``
        :param str layer_id: the id of the layer that this
          :paramref:`svg` should be placed inside

        """
        content = xmltodict.parse(svg)
        self.place_svg_dict(x, y, content, layer_id)