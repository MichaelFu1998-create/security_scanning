def draw(self):
        
        """ Draws the editable path and interface elements.
        """
                
        # Enable interaction.
        self.update()
        x, y = mouse()
        
        # Snap to grid when enabled.
        # The grid is enabled with the TAB key.
        if self.show_grid:
            self.grid.draw()
            x, y = self.grid.snap(x, y)
        
        _ctx.strokewidth(self.strokewidth)
        if self.freehand:
            self.draw_freehand()
        
        r = 4
        _ctx.nofill()
        if len(self._points) > 0:
            
            first = True            
            for i in range(len(self._points)):
                
                # Construct the path.
                pt = self._points[i]
                if first:
                    _ctx.beginpath(pt.x, pt.y)
                    first = False
                else:
                    if pt.cmd == CLOSE:
                        _ctx.closepath()
                    elif pt.cmd == MOVETO:
                        _ctx.moveto(pt.x, pt.y)
                    elif pt.cmd == LINETO:
                        _ctx.lineto(pt.x, pt.y)
                    elif pt.cmd == CURVETO:
                        _ctx.curveto(pt.ctrl1.x, pt.ctrl1.y, 
                                     pt.ctrl2.x, pt.ctrl2.y, 
                                     pt.x, pt.y)
                # In add- or edit-mode,
                # display the current point's handles.
                if ((i == self.edit and self.new == None) \
                or pt == self.new) \
                and pt.cmd == CURVETO \
                and not pt.freehand:
                    _ctx.stroke(self.handle_color)
                    _ctx.nofill()
                    _ctx.oval(pt.x-r, pt.y-r, r*2, r*2)
                    _ctx.stroke(self.handle_color)
                    _ctx.line(pt.ctrl2.x, pt.ctrl2.y, pt.x, pt.y)
                    _ctx.fill(self.handle_color)
                # Display the new point's handle being dragged.
                if pt == self.new \
                and not pt.freehand:
                    rx, ry = self.reflect(pt.x, pt.y, pt.ctrl2.x, pt.ctrl2.y)
                    _ctx.stroke(self.handle_color)
                    _ctx.line(rx, ry, pt.x, pt.y)
                    _ctx.nostroke()
                    _ctx.fill(self.handle_color)
                    _ctx.oval(rx-r/2, ry-r/2, r, r)
                # Display handles for point being edited.
                if i == self.edit \
                and self.new == None \
                and pt.cmd == CURVETO \
                and not pt.freehand:
                    _ctx.oval(pt.ctrl2.x-r/2, pt.ctrl2.y-r/2, r, r)
                    if i > 0:
                        prev = self._points[i-1]
                        _ctx.line(pt.ctrl1.x, pt.ctrl1.y, prev.x, prev.y)
                        _ctx.oval(pt.ctrl1.x-r/2, pt.ctrl1.y-r/2, r, r)
                    if i > 0 and self._points[i-1].cmd != MOVETO:
                        _ctx.line(prev.ctrl2.x, prev.ctrl2.y, prev.x, prev.y)
                    if i < len(self._points)-1:
                        next = self._points[i+1]
                        if next.cmd == CURVETO:
                            _ctx.line(next.ctrl1.x, next.ctrl1.y, pt.x, pt.y)
                
                # When hovering over a point,
                # highlight it.
                elif self.overlap(x, y, pt.x, pt.y) \
                and not pt.freehand:
                    self.insert = False # quit insert mode
                    _ctx.nofill()
                    _ctx.stroke(self.handle_color)
                    _ctx.oval(pt.x-r, pt.y-r, r*2, r*2)
                
                # Provide visual coordinates
                # for points being dragged, moved or hovered.
                _ctx.fontsize(9)
                _ctx.fill(self.handle_color)
                txt = " ("+str(int(pt.x))+", "+str(int(pt.y))+")"
                if (i == self.edit and self.new == None) \
                or pt == self.new \
                and not pt.freehand:
                    _ctx.text(txt, pt.x+r, pt.y+2)                                       
                elif self.overlap(x, y, pt.x, pt.y) \
                and not pt.freehand:
                    _ctx.text(txt, pt.x+r, pt.y+2)

                # Draw a circle for each point
                # in the path.
                if not pt.freehand:
                    if pt.cmd != MOVETO:
                        _ctx.fill(self.path_color)
                        _ctx.nostroke()
                    else:
                        _ctx.stroke(self.path_color)
                        _ctx.nofill()
                    _ctx.oval(pt.x-r/2, pt.y-r/2, r, r)
                
            # Draw the current path,
            # update the path property.
            _ctx.stroke(self.path_color)
            _ctx.fill(self.path_fill)
            _ctx.autoclosepath(False)    
            p = _ctx.endpath()
            self.path = p
            
            # Possible to insert a point here.
            if self.insert:
                _ctx.stroke(self.handle_color)
                _ctx.nofill()
                _ctx.oval(x-r*0.8, y-r*0.8, r*1.6, r*1.6)
                
            # When not editing a node,
            # prospect how the curve will continue
            # when adding a new point.
            if self.edit == None \
            and self.new == None \
            and self.moveto != True \
            and not self.freehand:
                _ctx.nofill()
                _ctx.stroke(self.new_color)
                rx, ry = self.reflect(pt.x, pt.y, pt.ctrl2.x, pt.ctrl2.y)
                _ctx.beginpath(pt.x, pt.y)
                _ctx.curveto(rx, ry, x, y, x, y)
                _ctx.endpath()

                # A dashed line indicates what
                # a CLOSETO would look like.
                if self.last_moveto != None:
                    start = self.last_moveto
                else:
                    start = self._points[0]
                p = _ctx.line(x, y, start.x, start.y, draw=False)
                try: p._nsBezierPath.setLineDash_count_phase_([2,4], 2, 50)
                except:
                    pass
                _ctx.drawpath(p)
        
            # When doing a MOVETO,
            # show the new point hovering at the mouse location.
            elif self.edit == None \
            and self.new == None \
            and self.moveto != None:
                _ctx.stroke(self.new_color)
                _ctx.nofill()
                _ctx.oval(x-r*0.8, y-r*0.8, r*1.6, r*1.6)
            
            # Draws button for a point being edited.
            # The first button deletes the point.
            # The second button, which appears only on the last point
            # in the path, tells the editor to perform a MOVETO
            # before adding a new point.
            if self.edit != None:
                pt = self._points[self.edit]
                x = pt.x + self.btn_x
                y = pt.y + self.btn_y
                r = self.btn_r
                _ctx.nostroke()
                _ctx.fill(0,0,0,0.2)
                _ctx.fill(self.handle_color)
                _ctx.oval(x-r, y-r, r*2, r*2)
                _ctx.fill(1)
                _ctx.rotate(45)
                _ctx.rect(x-r+2, y-0.625, r+1, 1.25)
                _ctx.rotate(-90)
                _ctx.rect(x-r+2, y-0.625, r+1, 1.25)
                _ctx.reset()
                if self.edit == len(self._points)-1:
                    _ctx.fill(self.handle_color)
                    _ctx.oval(x+r*2+2-r, y-r, r*2, r*2)
                    _ctx.fill(1)
                    _ctx.rect(x+r*2+2-2.25, y-r+3, 1.5, r-1)
                    _ctx.rect(x+r*2+2+0.75, y-r+3, 1.5, r-1)
        
        # Handle onscreen notifications.
        # Any text in msg is displayed in a box in the center
        # and slowly fades away, after which msg is cleared.    
        if self.msg != "":
            self.msg_alpha -= 0.1
            _ctx.nostroke()
            _ctx.fill(0,0,0, self.msg_alpha)
            _ctx.fontsize(18)
            _ctx.lineheight(1)
            w = _ctx.textwidth(self.msg)
            _ctx.rect(_ctx.WIDTH/2-w/2-9, _ctx.HEIGHT/2-27, w+18, 36, roundness=0.4)
            _ctx.fill(1,1,1, 0.8)
            _ctx.align(CENTER) 
            _ctx.text(self.msg, 0, _ctx.HEIGHT/2, width=_ctx.WIDTH)
        if self.msg_alpha <= 0.0:
            self.msg = ""
            self.msg_alpha = 1.0