def _interpolate(self, colors, n=100):

        """ Returns intermediary colors for given list of colors.
        """

        gradient = []
        for i in _range(n):
            l = len(colors) - 1
            x = int(1.0 * i / n * l)
            x = min(x + 0, l)
            y = min(x + 1, l)

            base = 1.0 * n / l * x
            d = (i - base) / (1.0 * n / l)
            r = colors[x].r * (1 - d) + colors[y].r * d
            g = colors[x].g * (1 - d) + colors[y].g * d
            b = colors[x].b * (1 - d) + colors[y].b * d
            a = colors[x].a * (1 - d) + colors[y].a * d

            gradient.append(color(r, g, b, a, mode="rgb"))

        gradient.append(colors[-1])
        return gradient