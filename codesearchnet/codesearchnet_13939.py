def contrast(self, value=1.0):
    
        """Increases or decreases the contrast in the layer.
    
        The given value is a percentage to increase
        or decrease the image contrast,
        for example 1.2 means contrast at 120%.
    
        """

        c = ImageEnhance.Contrast(self.img) 
        self.img = c.enhance(value)