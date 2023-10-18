def rotate(self, angle):
    
        """Rotates the layer.
    
        Rotates the layer by given angle.
        Positive numbers rotate counter-clockwise,
        negative numbers rotate clockwise.
    
        Rotate commands are executed instantly,
        so many subsequent rotates will distort the image.
    
        """
    
        #When a layer rotates, its corners will fall outside
        #of its defined width and height.
        #Thus, its bounding box needs to be expanded.
    
        #Calculate the diagonal width, and angle from the layer center.
        #This way we can use the layers's corners 
        #to calculate the bounding box.
    
        from math import sqrt, pow, sin, cos, degrees, radians, asin
        w0, h0 = self.img.size
        d = sqrt(pow(w0,2) + pow(h0,2))
        d_angle = degrees(asin((w0*0.5) / (d*0.5)))
    
        angle = angle % 360
        if angle > 90 and angle <= 270: d_angle += 180
    
        w = sin(radians(d_angle + angle)) * d
        w = max(w, sin(radians(d_angle - angle)) * d)
        w = int(abs(w))
    
        h = cos(radians(d_angle + angle)) * d
        h = max(h, cos(radians(d_angle - angle)) * d)
        h = int(abs(h))
    
        dx = int((w-w0) / 2)
        dy = int((h-h0) / 2)
        d = int(d)

        #The rotation box's background color
        #is the mean pixel value of the rotating image.
        #This is the best option to avoid borders around
        #the rotated image.

        bg = ImageStat.Stat(self.img).mean
        bg = (int(bg[0]), int(bg[1]), int(bg[2]), 0)

        box = Image.new("RGBA", (d,d), bg)
        box.paste(self.img, ((d-w0)/2, (d-h0)/2))
        box = box.rotate(angle, INTERPOLATION)
        box = box.crop(((d-w)/2+2, (d-h)/2, d-(d-w)/2, d-(d-h)/2))
        self.img = box
    
        #Since rotate changes the bounding box size,
        #update the layers' width, height, and position,
        #so it rotates from the center.
    
        self.x += (self.w-w)/2
        self.y += (self.h-h)/2
        self.w = w
        self.h = h