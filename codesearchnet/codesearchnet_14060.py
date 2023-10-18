def show(self, format='png', as_data=False):
        '''Returns an Image object of the current surface. Used for displaying
        output in Jupyter notebooks. Adapted from the cairo-jupyter project.'''

        from io import BytesIO

        b = BytesIO()

        if format == 'png':
            from IPython.display import Image
            surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.WIDTH, self.HEIGHT)
            self.snapshot(surface)
            surface.write_to_png(b)
            b.seek(0)
            data = b.read()
            if as_data:
                return data
            else:
                return Image(data)
        elif format == 'svg':
            from IPython.display import SVG
            surface = cairo.SVGSurface(b, self.WIDTH, self.HEIGHT)
            surface.finish()
            b.seek(0)
            data = b.read()
            if as_data:
                return data
            else:
                return SVG(data)