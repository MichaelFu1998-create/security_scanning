def arrow(self, x, y, width, type=NORMAL, draw=True, **kwargs):
        '''Draw an arrow.

        Arrows can be two types: NORMAL or FORTYFIVE.

        :param x: top left x-coordinate
        :param y: top left y-coordinate
        :param width: width of arrow
        :param type:  NORMAL or FORTYFIVE
        :draw:  If True draws arrow immediately

        :return: Path object representing the arrow.
        '''
        # Taken from Nodebox
        path = self.BezierPath(**kwargs)
        if type == self.NORMAL:
            head = width * .4
            tail = width * .2
            path.moveto(x, y)
            path.lineto(x - head, y + head)
            path.lineto(x - head, y + tail)
            path.lineto(x - width, y + tail)
            path.lineto(x - width, y - tail)
            path.lineto(x - head, y - tail)
            path.lineto(x - head, y - head)
            path.lineto(x, y)
        elif type == self.FORTYFIVE:
            head = .3
            tail = 1 + head
            path.moveto(x, y)
            path.lineto(x, y + width * (1 - head))
            path.lineto(x - width * head, y + width)
            path.lineto(x - width * head, y + width * tail * .4)
            path.lineto(x - width * tail * .6, y + width)
            path.lineto(x - width, y + width * tail * .6)
            path.lineto(x - width * tail * .4, y + width * head)
            path.lineto(x - width, y + width * head)
            path.lineto(x - width * (1 - head), y)
            path.lineto(x, y)
        else:
            raise NameError(_("arrow: available types for arrow() are NORMAL and FORTYFIVE\n"))
        if draw:
            path.draw()
        return path