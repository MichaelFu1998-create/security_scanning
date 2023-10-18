def export(self, filename):
    
        """Exports the flattened canvas.
    
        Flattens the canvas.
        PNG retains the alpha channel information.
        Other possibilities are JPEG and GIF.
    
        """

        self.flatten()
        self.layers[1].img.save(filename)
        return filename