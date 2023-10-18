def select(self, path, feather=True):
    
        """Applies the polygonal lasso tool on a layer.
    
        The path paramater is a list of points,
        either [x1, y1, x2, y2, x3, y3, ...]
        or [(x1,y1), (x2,y2), (x3,y3), ...]
    
        The parts of the layer that fall outside
        this polygonal area are cut.
        
        The selection is not anti-aliased,
        but the feather parameter creates soft edges.
    
        """
    
        w, h = self.img.size
        mask = Image.new("L", (w,h), 0)
        draw = ImageDraw.Draw(mask)
        
        draw = ImageDraw.Draw(mask)
        draw.polygon(path, fill=255)

        if feather:
            mask = mask.filter(ImageFilter.SMOOTH_MORE)
            mask = mask.filter(ImageFilter.SMOOTH_MORE)
            
        mask = ImageChops.darker(mask, self.img.split()[3])
        self.img.putalpha(mask)