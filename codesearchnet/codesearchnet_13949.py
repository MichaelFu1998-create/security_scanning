def overlay(self, img1, img2):
    
        """Applies the overlay blend mode.
    
        Overlays image img2 on image img1.
        The overlay pixel combines multiply and screen:
        it multiplies dark pixels values and screen light values.
        Returns a composite image with the alpha channel retained.
    
        """
    
        p1 = list(img1.getdata())
        p2 = list(img2.getdata())
    
        for i in range(len(p1)):
        
            p3 = ()
            for j in range(len(p1[i])):

                a = p1[i][j] / 255.0
                b = p2[i][j] / 255.0
            
                #When overlaying the alpha channels,
                #take the alpha of the most transparent layer.
            
                if j == 3:
                    #d = (a+b)*0.5
                    #d = a
                    d = min(a,b)
                elif a > 0.5: 
                    d = 2*(a+b-a*b)-1
                else: 
                    d = 2*a*b            
                p3 += (int(d*255),)
        
            p1[i] = p3
        
        img = Image.new("RGBA", img1.size, 255)
        img.putdata(p1)
        return img