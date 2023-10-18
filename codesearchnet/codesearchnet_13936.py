def mask(self):
    
        """Masks the layer below with this layer.
    
        Commits the current layer to the alpha channel of 
        the previous layer. Primarily, mask() is useful when 
        using gradient layers as masks on images below. 
    
        For example:
        canvas.layer("image.jpg")
        canvas.gradient()
        canvas.layer(2).flip()
        canvas.layer(2).mask()
    
        Adds a white-to-black linear gradient to
        the alpha channel of image.jpg, 
        making it evolve from opaque on 
        the left to transparent on the right.
    
        """

        if len(self.canvas.layers) < 2: return
        i = self.index()
        if i == 0: return
        
        layer = self.canvas.layers[i-1]
    
        alpha = Image.new("L", layer.img.size, 0)
    
        #Make a composite of the mask layer in grayscale
        #and its own alpha channel.
    
        mask = self.canvas.layers[i]        
        flat = ImageChops.darker(mask.img.convert("L"), mask.img.split()[3])
        alpha.paste(flat, (mask.x,mask.y))
        alpha = ImageChops.darker(alpha, layer.img.split()[3])
        layer.img.putalpha(alpha)
    
        self.delete()