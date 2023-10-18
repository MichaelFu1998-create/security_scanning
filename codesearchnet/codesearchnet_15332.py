def color(self, x, y, paint_method):
        """
        :param paint_method: 'point' or 'replace' or 'floodfill' or
                             'filltoborder' or 'reset'
        :type paint_method: str or pgmagick.PaintMethod
        """
        paint_method = _convert_paintmethod(paint_method)
        color = pgmagick.DrawableColor(x, y, paint_method)
        self.drawer.append(color)