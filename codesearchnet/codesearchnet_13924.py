def fill(self, rgb, x=0, y=0, w=None, h=None, name=""):
    
        """Creates a new fill layer.
    
        Creates a new layer filled with the given rgb color.
        For example, fill((255,0,0)) creates a red fill.
        The layers fills the entire canvas by default.
    
        """ 
    
        if w == None: w = self.w - x
        if h == None: h = self.h - y
        img = Image.new("RGBA", (w,h), rgb)
        self.layer(img, x, y, name)