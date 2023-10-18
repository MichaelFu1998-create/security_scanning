def _get_contours(self):
        """
        Returns a list of contours in the path, as BezierPath objects.
        A contour is a sequence of lines and curves separated from the next contour by a MOVETO.
        For example, the glyph "o" has two contours: the inner circle and the outer circle.
        """
        # Originally from nodebox-gl
        contours = []
        current_contour = None
        empty = True
        for i, el in enumerate(self._get_elements()):
            if el.cmd == MOVETO:
                if not empty:
                    contours.append(current_contour)
                current_contour = BezierPath(self._bot)
                current_contour.moveto(el.x, el.y)
                empty = True
            elif el.cmd == LINETO:
                empty = False
                current_contour.lineto(el.x, el.y)
            elif el.cmd == CURVETO:
                empty = False
                current_contour.curveto(el.c1x, el.c1y, el.c2x, el.c2y, el.x, el.y)
            elif el.cmd == CLOSE:
                current_contour.closepath()
        if not empty:
            contours.append(current_contour)
        return contours