def duplicate(self):
    
        """Creates a copy of the current layer.
    
        This copy becomes the top layer on the canvas.
    
        """
    
        i = self.canvas.layer(self.img.copy(), self.x, self.y, self.name)
        clone = self.canvas.layers[i]
        clone.alpha = self.alpha
        clone.blend = self.blend