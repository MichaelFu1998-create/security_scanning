def text(self, txt, x, y, width=None, height=1000000, outline=False, draw=True, **kwargs):
        '''
        Draws a string of text according to current font settings.

        :param txt: Text to output
        :param x: x-coordinate of the top left corner
        :param y: y-coordinate of the top left corner
        :param width: text width
        :param height: text height
        :param outline: If True draws outline text (defaults to False)
        :param draw: Set to False to inhibit immediate drawing (defaults to True)
        :return: Path object representing the text.
        '''
        txt = self.Text(txt, x, y, width, height, outline=outline, ctx=None, **kwargs)
        if outline:
            path = txt.path
            if draw:
                path.draw()
            return path
        else:
            return txt