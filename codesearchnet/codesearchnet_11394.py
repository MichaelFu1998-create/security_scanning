def color_ramp(self, size):
        """Generate a color ramp for the current screen height."""
        color = PALETTE.get(self.option.palette, {})
        color = color.get(self.term.colors, None)
        color_ramp = []
        if color is not None:
            ratio = len(color) / float(size)
            for i in range(int(size)):
                color_ramp.append(self.term.color(color[int(ratio * i)]))

        return color_ramp