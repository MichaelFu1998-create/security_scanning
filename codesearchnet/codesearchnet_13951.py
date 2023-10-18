def convolute(self, kernel, scale=None, offset=0):
        
        """A (3,3) or (5,5) convolution kernel.
        
        The kernel argument is a list with either 9 or 25 elements,
        the weight for each surrounding pixels to convolute.
        
        """
        
        if len(kernel)   ==  9: size = (3,3)
        elif len(kernel) == 25: size = (5,5)
        else: return
        
        if scale == None:
            scale = 0
            for x in kernel: scale += x
            if scale == 0: scale = 1
     
        f = ImageFilter.BuiltinFilter()
        f.filterargs = size, scale, offset, kernel
        self.layer.img = self.layer.img.filter(f)