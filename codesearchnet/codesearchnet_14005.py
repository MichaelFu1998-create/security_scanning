def offset(self, node):
        """ Returns the distance from the center to the given node.
        """
        x = self.x + node.x - _ctx.WIDTH/2
        y = self.y + node.y - _ctx.HEIGHT/2
        return x, y