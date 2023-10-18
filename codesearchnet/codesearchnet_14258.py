def rendering_finished(self, size, frame, cairo_ctx):
        """
        Called when CairoCanvas has rendered a bot
        """
        surface = cairo_ctx.get_target()
        if self.format == 'png':
            surface.write_to_png(self._output_file(frame))
        surface.finish()
        surface.flush()