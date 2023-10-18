def _get_center(self):
        '''Returns the center point of the path, disregarding transforms.
        '''
        x = (self.x + self.width / 2)
        y = (self.y + self.height / 2)
        return (x, y)