def matte(self, x, y, paint_method):
        """
        :param paint_method: 'point' or 'replace' or 'floodfill' or
                             'filltoborder' or 'reset'
        :type paint_method: str or pgmagick.PaintMethod
        """
        paint_method = _convert_paintmethod(paint_method)
        self.drawer.append(pgmagick.DrawableMatte(x, y, paint_method))