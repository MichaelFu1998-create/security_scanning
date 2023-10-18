def desaturate(self):
    
        """Desaturates the layer, making it grayscale.
    
        Instantly removes all color information from the layer,
        while maintaing its alpha channel.
    
        """
    
        alpha = self.img.split()[3]
        self.img = self.img.convert("L")
        self.img = self.img.convert("RGBA")
        self.img.putalpha(alpha)