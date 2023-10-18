def _get_center(self):
        '''Returns the center point of the path, disregarding transforms.
        '''
        w, h = self.layout.get_pixel_size()
        x = (self.x + w / 2)
        y = (self.y + h / 2)
        return x, y