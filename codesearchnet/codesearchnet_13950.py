def hue(self, img1, img2):
    
        """Applies the hue blend mode.
    
        Hues image img1 with image img2.
        The hue filter replaces the hues of pixels in img1
        with the hues of pixels in img2.
        Returns a composite image with the alpha channel retained.
    
        """

        import colorsys

        p1 = list(img1.getdata())
        p2 = list(img2.getdata())
        for i in range(len(p1)):
        
            r1, g1, b1, a1 = p1[i]
            r1 = r1 / 255.0
            g1 = g1 / 255.0
            b1 = b1 / 255.0
        
            h1, s1, v1 = colorsys.rgb_to_hsv(r1, g1, b1)
        
            r2, g2, b2, a2 = p2[i]
            r2 = r2 / 255.0
            g2 = g2 / 255.0
            b2 = b2 / 255.0
            h2, s2, v2 = colorsys.rgb_to_hsv(r2, g2, b2)
        
            r3, g3, b3 = colorsys.hsv_to_rgb(h2, s1, v1)
        
            r3 = int(r3*255)
            g3 = int(g3*255)
            b3 = int(b3*255)
            p1[i] = (r3, g3, b3, a1)
    
        img = Image.new("RGBA", img1.size, 255)
        img.putdata(p1)
        return img