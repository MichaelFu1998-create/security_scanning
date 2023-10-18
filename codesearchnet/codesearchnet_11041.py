def clear(self):
        """
        Clear the window buffer
        """
        self.ctx.fbo.clear(
            red=self.clear_color[0],
            green=self.clear_color[1],
            blue=self.clear_color[2],
            alpha=self.clear_color[3],
            depth=self.clear_depth,
        )