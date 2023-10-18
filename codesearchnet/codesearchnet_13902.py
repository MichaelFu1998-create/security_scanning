def transform_path(self, path):
        """ Returns a BezierPath object with the transformation applied.
        """
        p = path.__class__() # Create a new BezierPath.
        for pt in path:
            if pt.cmd == "close":
                p.closepath()
            elif pt.cmd == "moveto":
                p.moveto(*self.apply(pt.x, pt.y))
            elif pt.cmd == "lineto":
                p.lineto(*self.apply(pt.x, pt.y))
            elif pt.cmd == "curveto":
                vx1, vy1 = self.apply(pt.ctrl1.x, pt.ctrl1.y)
                vx2, vy2 = self.apply(pt.ctrl2.x, pt.ctrl2.y)
                x, y = self.apply(pt.x, pt.y)
                p.curveto(vx1, vy1, vx2, vy2, x, y)
        return p