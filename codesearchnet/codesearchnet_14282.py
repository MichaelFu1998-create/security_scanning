def draw(self):
        
        """ Draws a popup rectangle with a rotating text queue.        
        """ 
        
        if len(self.q) > 0:
            self.update()
            
            if self.delay == 0:
                
                # Rounded rectangle in the given background color.
                p, h = self.textpath(self.i)
                f = self.fontsize
                self._ctx.fill(self.background)
                self._ctx.rect(
                    self.node.x + f*1.0, 
                    self.node.y + f*0.5, 
                    self._w + f, 
                    h + f*1.5, 
                    roundness=0.2
                )
                
                # Fade in/out the current text.
                alpha = 1.0
                if self.fi < 5: 
                    alpha = 0.2 * self.fi
                if self.fn-self.fi < 5: 
                    alpha = 0.2 * (self.fn-self.fi)
                self._ctx.fill(
                    self.text.r,
                    self.text.g,
                    self.text.b,
                    self.text.a * alpha
                )
                
                self._ctx.translate(self.node.x + f*2.0, self.node.y + f*2.5)
                self._ctx.drawpath(p)