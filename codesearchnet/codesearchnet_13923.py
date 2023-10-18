def layer(self, img, x=0, y=0, name=""):
    
        """Creates a new layer from file, Layer, PIL Image.
    
        If img is an image file or PIL Image object,
        Creates a new layer with the given image file.
        The image is positioned on the canvas at x, y.
        
        If img is a Layer,
        uses that layer's x and y position and name.
    
        """

        from types import StringType
        if isinstance(img, Image.Image):
            img = img.convert("RGBA")
            self.layers.append(Layer(self, img, x, y, name))
            return len(self.layers)-1
        if isinstance(img, Layer):
            img.canvas = self
            self.layers.append(img)
            return len(self.layers)-1                 
        if type(img) == StringType: 
            img = Image.open(img)
            img = img.convert("RGBA")
            self.layers.append(Layer(self, img, x, y, name))
            return len(self.layers)-1