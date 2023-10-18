def drag(self, node):

        """ Drags given node to mouse location.
        """
    
        dx = self.mouse.x - self.graph.x
        dy = self.mouse.y - self.graph.y

        # A dashed line indicates the drag vector.
        s = self.graph.styles.default
        self._ctx.nofill()
        self._ctx.nostroke()
        if s.stroke: 
            self._ctx.strokewidth(s.strokewidth)
            self._ctx.stroke(
                s.stroke.r, 
                s.stroke.g, 
                s.stroke.g, 
                0.75
            )
        p = self._ctx.line(node.x, node.y, dx, dy, draw=False)
        try: p._nsBezierPath.setLineDash_count_phase_([2,4], 2, 50)
        except:
            pass
        self._ctx.drawpath(p)
        r = node.__class__(None).r * 0.75
        self._ctx.oval(dx-r/2, dy-r/2, r, r)
    
        node.vx = dx / self.graph.d
        node.vy = dy / self.graph.d