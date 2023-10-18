def delete(self):
        
        """Removes this layer from the canvas.
              
        """
        
        i = self.index()
        if i != None: del self.canvas.layers[i]