def index(self):
        
        """Returns this layer's index in the canvas.layers[].
        
        Searches the position of this layer in the canvas'
        layers list, return None when not found.
        
        """
        
        for i in range(len(self.canvas.layers)):
            if self.canvas.layers[i] == self: break
        if self.canvas.layers[i] == self: 
            return i
        else:
            return None