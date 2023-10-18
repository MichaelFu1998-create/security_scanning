def kivy_svg(self):
        """An SVG object.

        :return: an SVG object
        :rtype: kivy.graphics.svg.Svg
        :raises ImportError: if the module was not found
        """
        from kivy.graphics.svg import Svg
        path = self.temporary_path(".svg")
        try:
            return Svg(path)
        finally:
            remove_file(path)