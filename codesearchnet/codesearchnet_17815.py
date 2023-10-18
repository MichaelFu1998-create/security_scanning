def connect(self, axis0, n0_index, source_angle, axis1, n1_index, target_angle, **kwargs):
        """Draw edges as Bézier curves.

        Start and end points map to the coordinates of the given nodes
        which in turn are set when adding nodes to an axis with the
        Axis.add_node() method, by using the placement information of
        the axis and a specified offset from its start point.
        
        Control points are set at the same distance from the start (or end)
        point of an axis as their corresponding nodes, but along an invisible
        axis that shares its origin but diverges by a given angle.


        Parameters
        ----------
        axis0        : source Axis object
        n0_index     : key of source node in nodes dictionary of axis0
        source_angle : angle of departure for invisible axis that diverges from axis0 and holds first control points
        axis1        : target Axis object
        n1_index     : key of target node in nodes dictionary of axis1
        target_angle : angle of departure for invisible axis that diverges from axis1 and holds second control points
        kwargs       : extra SVG attributes for path element, optional
                       Set or change attributes using key=value

        """        
        n0    = axis0.nodes[n0_index]
        n1    = axis1.nodes[n1_index]

        pth  = self.dwg.path(d="M %s %s" % (n0.x, n0.y), fill='none', **kwargs) # source

        # compute source control point
        alfa = axis0.angle() + radians(source_angle)
        length = sqrt( ((n0.x - axis0.start[0])**2) + ((n0.y-axis0.start[1])**2)) 
        x = axis0.start[0] + length * cos(alfa);
        y = axis0.start[1] + length * sin(alfa);

        pth.push("C %s %s" % (x, y)) # first control point in path

        # compute target control point
        alfa = axis1.angle() + radians(target_angle)
        length = sqrt( ((n1.x - axis1.start[0])**2) + ((n1.y-axis1.start[1])**2)) 
        x = axis1.start[0] + length * cos(alfa);
        y = axis1.start[1] + length * sin(alfa);
        
        pth.push("%s %s" % (x, y))   # second control point in path

        pth.push("%s %s" % (n1.x, n1.y)) # target
        self.dwg.add(pth)