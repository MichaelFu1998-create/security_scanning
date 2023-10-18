def GetPixelColorsOfRects(self, rects: list) -> list:
        """
        rects: a list of rects, such as [(0,0,10,10), (10,10,20,20),(x,y,width,height)].
        Return list, a list whose elements are ctypes.Array which is an iterable array of int values in argb.
        """
        rects2 = [(x, y, x + width, y + height) for x, y, width, height in rects]
        left, top, right, bottom = zip(*rects2)
        left, top, right, bottom = min(left), min(top), max(right), max(bottom)
        width, height = right - left, bottom - top
        allColors = self.GetPixelColorsOfRect(left, top, width, height)
        colorsOfRects = []
        for x, y, w, h in rects:
            x -= left
            y -= top
            colors = []
            for row in range(h):
                colors.extend(allColors[(y + row) * width + x:(y + row) * width + x + w])
            colorsOfRects.append(colors)
        return colorsOfRects