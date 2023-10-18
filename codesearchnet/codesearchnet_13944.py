def distort(self, x1=0,y1=0, x2=0,y2=0, x3=0,y3=0, x4=0,y4=0):
    
        """Distorts the layer.
        
        Distorts the layer by translating 
        the four corners of its bounding box to the given coordinates:
        upper left (x1,y1), upper right(x2,y2),
        lower right (x3,y3) and lower left (x4,y4).
        
        """
    
        w, h = self.img.size
        quad = (-x1,-y1, -x4,h-y4, w-x3,w-y3, w-x2,-y2)
        self.img = self.img.transform(self.img.size, Image.QUAD, quad, INTERPOLATION)