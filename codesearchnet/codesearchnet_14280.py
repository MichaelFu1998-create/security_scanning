def textpath(self, i):
        
        """ Returns a cached textpath of the given text in queue.
        """
        
        if len(self._textpaths) == i:
            self._ctx.font(self.font, self.fontsize)
            txt = self.q[i]
            if len(self.q) > 1:
                # Indicate current text (e.g. 5/13).
                txt += " ("+str(i+1)+"/" + str(len(self.q))+")"
            p = self._ctx.textpath(txt, 0, 0, width=self._w)
            h = self._ctx.textheight(txt, width=self._w)
            self._textpaths.append((p, h))

        return self._textpaths[i]