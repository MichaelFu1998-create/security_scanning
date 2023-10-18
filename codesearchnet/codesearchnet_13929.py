def draw(self, x, y):
        
        """Places the flattened canvas in NodeBox.
        
        Exports to a temporary PNG file.
        Draws the PNG in NodeBox using the image() command.
        Removes the temporary file.
        
        """
        
        try:
            from time import time
            import md5
            from os import unlink
            m = md5.new()
            m.update(str(time()))
            filename = "photobot" + str(m.hexdigest()) + ".png"
            self.export(filename)
            _ctx.image(filename, x, y)
            unlink(filename)
        
        except:
            pass