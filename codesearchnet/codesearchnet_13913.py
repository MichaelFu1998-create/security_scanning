def textpath(self, txt, x, y, width=None, height=1000000, enableRendering=False, **kwargs):
        '''
        Draws an outlined path of the input text
        '''
        txt = self.Text(txt, x, y, width, height, **kwargs)
        path = txt.path
        if draw:
            path.draw()
        return path