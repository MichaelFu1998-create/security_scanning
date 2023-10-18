def _set_fills_in_color_layer(self, svg_string, color):
        """replaces fill colors in ``<g inkscape:label="color"
        inkscape:groupmode="layer">`` with :paramref:`color`

        :param color: a color fill the objects in the layer with
        """
        structure = xmltodict.parse(svg_string)
        if color is None:
            return structure
        layers = structure["svg"]["g"]
        if not isinstance(layers, list):
            layers = [layers]
        for layer in layers:
            if not isinstance(layer, dict):
                continue
            if layer.get("@inkscape:label") == "color" and \
                    layer.get("@inkscape:groupmode") == "layer":
                for key, elements in layer.items():
                    if key.startswith("@") or key.startswith("#"):
                        continue
                    if not isinstance(elements, list):
                        elements = [elements]
                    for element in elements:
                        style = element.get("@style", None)
                        if style:
                            style = style.split(";")
                            processed_style = []
                            for style_element in style:
                                if style_element.startswith("fill:"):
                                    style_element = "fill:" + color
                                processed_style.append(style_element)
                            style = ";".join(processed_style)
                            element["@style"] = style
        return structure