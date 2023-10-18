def draw_freehand(self):
        
        """ Freehand sketching.
        """
        
        if _ctx._ns["mousedown"]:
            
            x, y = mouse()
            if self.show_grid:
                x, y = self.grid.snap(x, y)
            
            if self.freehand_move == True:
                cmd = MOVETO
                self.freehand_move = False
            else:
                cmd = LINETO
            
            # Add a new LINETO to the path,
            # except when starting to draw,
            # then a MOVETO is added to the path.
            pt = PathElement()
            if cmd != MOVETO:
                pt.freehand = True # Used when mixed with curve drawing.
            else:
                pt.freehand = False
            pt.cmd = cmd
            pt.x = x
            pt.y = y
            pt.ctrl1 = Point(x,y)
            pt.ctrl2 = Point(x,y)
            self._points.append(pt)
            
            # Draw the current location of the cursor.
            r = 4
            _ctx.nofill()
            _ctx.stroke(self.handle_color)
            _ctx.oval(pt.x-r, pt.y-r, r*2, r*2)
            _ctx.fontsize(9)
            _ctx.fill(self.handle_color)
            _ctx.text(" ("+str(int(pt.x))+", "+str(int(pt.y))+")", pt.x+r, pt.y)
        
            self._dirty = True
        
        else:

            # Export the updated drawing,
            # remember to do a MOVETO on the next interaction.
            self.freehand_move = True
            if self._dirty:
                self._points[-1].freehand = False
                self.export_svg()
                self._dirty = False