def render(self, stream):
        """Render graph to stream."""
        encoding = self.option.encoding or self.term.encoding or "utf8"

        if self.option.color:
            ramp = self.color_ramp(self.size.y)[::-1]
        else:
            ramp = None

        if self.cycle >= 1 and self.lines:
            stream.write(self.term.csi('cuu', self.lines))

        zero = int(self.null / 4)  # Zero crossing
        lines = 0
        for y in range(self.screen.size.y):
            if y == zero and self.size.y > 1:
                stream.write(self.term.csi('smul'))
            if ramp:
                stream.write(ramp[y])

            for x in range(self.screen.size.x):
                point = Point((x, y))
                if point in self.screen:
                    value = self.screen[point]
                    if isinstance(value, int):
                        stream.write(chr(self.base + value).encode(encoding))
                    else:
                        stream.write(self.term.csi('sgr0'))
                        stream.write(self.term.csi_wrap(
                            value.encode(encoding),
                            'bold'
                        ))
                        if y == zero and self.size.y > 1:
                            stream.write(self.term.csi('smul'))
                        if ramp:
                            stream.write(ramp[y])
                else:
                    stream.write(b' ')

            if y == zero and self.size.y > 1:
                stream.write(self.term.csi('rmul'))
            if ramp:
                stream.write(self.term.csi('sgr0'))

            stream.write(b'\n')
            lines += 1
        stream.flush()

        self.cycle = self.cycle + 1
        self.lines = lines