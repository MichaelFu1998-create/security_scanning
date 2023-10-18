def ellipse(self, x, y, width, height, draw=True, **kwargs):
        '''Draws an ellipse starting from (x,y)'''
        path = self.BezierPath(**kwargs)
        path.ellipse(x,y,width,height)
        if draw:
            path.draw()
        return path