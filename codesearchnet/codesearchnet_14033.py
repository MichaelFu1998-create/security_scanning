def insert_point(self, x, y):
        
        """ Inserts a point on the path at the mouse location.
        
        We first need to check if the mouse location is on the path.
        Inserting point is time intensive and experimental.
        
        """
        
        try: 
            bezier = _ctx.ximport("bezier")
        except:
            from nodebox.graphics import bezier
        
        # Do a number of checks distributed along the path.
        # Keep the one closest to the actual mouse location.
        # Ten checks works fast but leads to imprecision in sharp corners
        # and curves closely located next to each other.
        # I prefer the slower but more stable approach.
        n = 100
        closest = None
        dx0 = float("inf") 
        dy0 = float("inf")
        for i in range(n):
            t = float(i)/n
            pt = self.path.point(t)
            dx = abs(pt.x-x)
            dy = abs(pt.y-y)
            if dx+dy <= dx0+dy0:
                dx0 = dx
                dy0 = dy
                closest = t

        # Next, scan the area around the approximation.
        # If the closest point is located at 0.2 on the path,
        # we need to scan between 0.1 and 0.3 for a better
        # approximation. If 1.5 was the best guess, scan
        # 1.40, 1.41 ... 1.59 and so on.
        # Each decimal precision takes 20 iterations.                
        decimals = [3,4]
        for d in decimals:
            d = 1.0/pow(10,d)
            
            for i in range(20):
                t = closest-d + float(i)*d*0.1
                if t < 0.0: t = 1.0+t
                if t > 1.0: t = t-1.0
                pt = self.path.point(t)
                dx = abs(pt.x-x)
                dy = abs(pt.y-y)
                if dx <= dx0 and dy <= dy0:
                    dx0 = dx
                    dy0 = dy
                    closest_precise = t
            
            closest = closest_precise   

        # Update the points list with the inserted point.
        p = bezier.insert_point(self.path, closest_precise)
        i, t, pt = bezier._locate(self.path, closest_precise)
        i += 1
        pt = PathElement()
        pt.cmd = p[i].cmd
        pt.x = p[i].x
        pt.y = p[i].y
        pt.ctrl1 = Point(p[i].ctrl1.x, p[i].ctrl1.y)
        pt.ctrl2 = Point(p[i].ctrl2.x, p[i].ctrl2.y)
        pt.freehand = False
        self._points.insert(i, pt)
        self._points[i-1].ctrl1 = Point(p[i-1].ctrl1.x, p[i-1].ctrl1.y)
        self._points[i+1].ctrl1 = Point(p[i+1].ctrl1.x, p[i+1].ctrl1.y)
        self._points[i+1].ctrl2 = Point(p[i+1].ctrl2.x, p[i+1].ctrl2.y)