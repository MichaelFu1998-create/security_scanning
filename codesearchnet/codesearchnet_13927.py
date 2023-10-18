def flatten(self, layers=[]):
    
        """Flattens all layers according to their blend modes.
    
        Merges all layers to the canvas,
        using the blend mode and opacity defined for each layer.
        Once flattened, the stack of layers is emptied except
        for the transparent background (bottom layer).
    
        """
        
        #When the layers argument is omitted,
        #flattens all the layers on the canvas.
        #When given, merges the indexed layers.
        
        #Layers that fall outside of the canvas are cropped:
        #this should be fixed by merging to a transparent background
        #large enough to hold all the given layers' data
        #(=time consuming).
        
        if layers == []: 
            layers = range(1, len(self.layers))
        background = self.layers._get_bg()
        background.name = "Background"
        
        for i in layers:

            layer = self.layers[i]
        
            #Determine which portion of the canvas
            #needs to be updated with the overlaying layer.
        
            x = max(0, layer.x)
            y = max(0, layer.y)
            w = min(background.w, layer.x+layer.w)
            h = min(background.h, layer.y+layer.h)
        
            base = background.img.crop((x, y, w, h))

            #Determine which piece of the layer
            #falls within the canvas.

            x = max(0, -layer.x)
            y = max(0, -layer.y)
            w -= layer.x
            h -= layer.y

            blend = layer.img.crop((x, y, w, h))
        
            #Buffer layer blend modes:
            #the base below is a flattened version
            #of all the layers below this one,
            #on which to merge this blended layer.
        
            if layer.blend == NORMAL:
                buffer = blend
            if layer.blend == MULTIPLY:
                buffer = ImageChops.multiply(base, blend)
            if layer.blend == SCREEN:
                buffer = ImageChops.screen(base, blend)
            if layer.blend == OVERLAY:
                buffer = Blend().overlay(base, blend)
            if layer.blend == HUE:
                buffer = Blend().hue(base, blend)
            if layer.blend == COLOR:
                buffer = Blend().color(base, blend)
            
            #Buffer a merge between the base and blend
            #according to the blend's alpha channel:
            #the base shines through where the blend is less opaque.
        
            #Merging the first layer to the transparent canvas
            #works slightly different than the other layers.
        
            alpha = buffer.split()[3]
            if i == 1:
                buffer = Image.composite(base, buffer, base.split()[3])
            else:
                buffer = Image.composite(buffer, base, alpha)
        
            #The alpha channel becomes a composite of
            #this layer and the base:
            #the base's (optional) tranparent background
            #is retained in arrays where the blend layer
            #is transparent as well.
        
            alpha = ImageChops.lighter(alpha, base.split()[3])
            buffer.putalpha(alpha)
        
            #Apply the layer's opacity,
            #merging the buffer to the base with
            #the given layer opacity.
        
            base = Image.blend(base, buffer, layer.alpha)

            #Merge the base to the flattened canvas.

            x = max(0, layer.x)
            y = max(0, layer.y)
            background.img.paste(base, (x,y))
    
        layers.reverse()
        for i in layers: del self.layers[i]
    
        img = Image.new("RGBA", (self.w,self.h), (255,255,255,0))
        self.layers._set_bg(Layer(self, img, 0, 0, name="_bg"))
        
        if len(self.layers) == 1:
            self.layers.append(background)
        else:
            self.layers.insert(layers[-1], background)