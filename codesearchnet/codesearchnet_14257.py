def create_rcontext(self, size, frame):
        """
        Called when CairoCanvas needs a cairo context to draw on
        """
        if self.format == 'pdf':
            surface = cairo.PDFSurface(self._output_file(frame), *size)
        elif self.format in ('ps', 'eps'):
            surface = cairo.PSSurface(self._output_file(frame), *size)
        elif self.format == 'svg':
            surface = cairo.SVGSurface(self._output_file(frame), *size)
        elif self.format == 'surface':
            surface = self.target
        else:
            surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, *size)
        return cairo.Context(surface)