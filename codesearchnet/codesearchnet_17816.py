def add_node(self, node, offset):
        """Add a Node object to nodes dictionary, calculating its coordinates using offset

        Parameters
        ----------
        node   : a Node object
        offset : float 
                 number between 0 and 1 that sets the distance
                 from the start point at which the node will be placed

        """
        # calculate x,y from offset considering axis start and end points
        width  = self.end[0] - self.start[0]
        height = self.end[1] - self.start[1]        
        node.x = self.start[0] + (width * offset)
        node.y = self.start[1] + (height * offset)
        self.nodes[node.ID] = node