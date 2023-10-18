def gradient(self, style=LINEAR, w=1.0, h=1.0, name=""):
    
        """Creates a gradient layer.
    
        Creates a gradient layer, that is usually used
        together with the mask() function.
    
        All the image functions work on gradients,
        so they can easily be flipped, rotated, scaled, inverted,
        made brighter or darker, ...
    
        Styles for gradients are LINEAR, RADIAL and DIAMOND.
    
        """
    
        from types import FloatType
        w0 = self.w 
        h0 = self.h
        if type(w) == FloatType: w *= w0
        if type(h) == FloatType: h *= h0
    
        img = Image.new("L", (int(w),int(h)), 255)
        draw = ImageDraw.Draw(img)
    
        if style == LINEAR:
            for i in range(int(w)):
                k = 255.0 * i/w
                draw.rectangle((i, 0, i, h), fill=int(k))
            
        if style == RADIAL:
            r = min(w,h)/2
            for i in range(int(r)):
                k = 255 - 255.0 * i/r
                draw.ellipse((w/2-r+i, h/2-r+i, w/2+r-i, h/2+r-i), fill=int(k))
            
        if style == DIAMOND:
            r = max(w,h)
            for i in range(int(r)):
                x = int(i*w/r*0.5)
                y = int(i*h/r*0.5)
                k = 255.0 * i/r
                draw.rectangle((x, y, w-x, h-y), outline=int(k))
    
        img = img.convert("RGBA")
        self.layer(img, 0, 0, name="")