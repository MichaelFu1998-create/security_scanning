def flip(self, axis=HORIZONTAL):
    
        """Flips the layer, either HORIZONTAL or VERTICAL.
    
        """

        if axis == HORIZONTAL:
            self.img = self.img.transpose(Image.FLIP_LEFT_RIGHT)
        if axis == VERTICAL:
            self.img = self.img.transpose(Image.FLIP_TOP_BOTTOM)