def invert(self):
    
        """Inverts the layer.
    
        """
    
        alpha = self.img.split()[3]
        self.img = self.img.convert("RGB")
        self.img = ImageOps.invert(self.img)
        self.img = self.img.convert("RGBA")
        self.img.putalpha(alpha)