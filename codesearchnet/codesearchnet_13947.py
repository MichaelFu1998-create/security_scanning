def sharpen(self, value=1.0):

        """Increases or decreases the sharpness in the layer.
    
        The given value is a percentage to increase
        or decrease the image sharpness,
        for example 0.8 means sharpness at 80%.
    
        """
     
        s = ImageEnhance.Sharpness(self.img) 
        self.img = s.enhance(value)