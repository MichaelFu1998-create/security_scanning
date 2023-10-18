def scale(self, w=1.0, h=1.0):
    
        """Resizes the layer to the given width and height.
    
        When width w or height h is a floating-point number,
        scales percentual, 
        otherwise scales to the given size in pixels.
    
        """

        from types import FloatType
        w0, h0 = self.img.size
        if type(w) == FloatType: w = int(w*w0)
        if type(h) == FloatType: h = int(h*h0)
    
        self.img = self.img.resize((w,h), INTERPOLATION)
        self.w = w
        self.h = h