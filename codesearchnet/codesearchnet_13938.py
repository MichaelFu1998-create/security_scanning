def brightness(self, value=1.0):

        """Increases or decreases the brightness in the layer.
    
        The given value is a percentage to increase
        or decrease the image brightness,
        for example 0.8 means brightness at 80%.
    
        """
     
        b = ImageEnhance.Brightness(self.img) 
        self.img = b.enhance(value)