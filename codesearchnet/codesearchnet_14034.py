def update(self):
        
        """ Update runs each frame to check for mouse interaction.
        
        Alters the path by allowing the user to add new points,
        drag point handles and move their location.
        Updates are automatically stored as SVG
        in the given filename.
        
        """
        
        x, y = mouse()
        if self.show_grid:
            x, y = self.grid.snap(x, y)
        
        if _ctx._ns["mousedown"] \
        and not self.freehand:
            
            self._dirty = True
            
            # Handle buttons first.
            # When pressing down on a button, all other action halts.
            # Buttons appear near a point being edited.
            # Once clicked, actions are resolved.
            if self.edit != None \
            and not self.drag_point \
            and not self.drag_handle1 \
            and not self.drag_handle2:
                pt = self._points[self.edit]
                dx = pt.x+self.btn_x
                dy = pt.y+self.btn_y
                # The delete button
                if self.overlap(dx, dy, x, y, r=self.btn_r):
                    self.delete = self.edit
                    return
                # The moveto button,
                # active on the last point in the path.
                dx += self.btn_r*2 + 2
                if self.edit == len(self._points) -1 and \
                   self.overlap(dx, dy, x, y, r=self.btn_r):
                    self.moveto = self.edit
                    return
                    
            if self.insert:
                self.inserting = True
                return
            
            # When not dragging a point or the handle of a point,
            # i.e. the mousebutton was released and then pressed again,
            # check to see if a point on the path is pressed.
            # When this point is not the last new point,
            # enter edit mode.
            if not self.drag_point and \
               not self.drag_handle1 and \
               not self.drag_handle2:
                self.editing = False
                indices = range(len(self._points))
                indices.reverse()
                for i in indices:
                    pt = self._points[i]
                    if pt != self.new \
                    and self.overlap(x, y, pt.x, pt.y) \
                    and self.new == None:
                        # Don't select a point if in fact
                        # it is at the same location of the first handle 
                        # of the point we are currently editing.
                        if self.edit == i+1 \
                        and self.overlap(self._points[i+1].ctrl1.x,
                                         self._points[i+1].ctrl1.y, x, y):
                            continue
                        else:
                            self.edit = i
                            self.editing = True
                            break
            
            # When the mouse button is down,
            # edit mode continues as long as
            # a point or handle is dragged.
            # Else, stop editing and switch to add-mode
            # (the user is clicking somewhere on the canvas).
            if not self.editing:
                if self.edit != None:
                    pt = self._points[self.edit]
                    if self.overlap(pt.ctrl1.x, pt.ctrl1.y, x, y) or \
                       self.overlap(pt.ctrl2.x, pt.ctrl2.y, x, y):
                        self.editing = True
                    else:
                        self.edit = None
                    
            # When not in edit mode, there are two options.
            # Either no new point is defined and the user is
            # clicking somewhere on the canvas (add a new point)
            # or the user is dragging the handle of the new point.
            # Adding a new point is a fluid click-to-locate and
            # drag-to-curve action.
            if self.edit == None:
                if self.new == None:
                    # A special case is when the used clicked
                    # the moveto button on the last point in the path.
                    # This indicates a gap (i.e. MOVETO) in the path.
                    self.new = PathElement()
                    if self.moveto == True \
                    or len(self._points) == 0:
                        cmd = MOVETO
                        self.moveto = None
                        self.last_moveto = self.new
                    else:
                        cmd = CURVETO
                    self.new.cmd = cmd
                    self.new.x = x
                    self.new.y = y
                    self.new.ctrl1 = Point(x, y)
                    self.new.ctrl2 = Point(x, y)
                    self.new.freehand = False
                    # Don't forget to map the point's ctrl1 handle
                    # to the ctrl2 handle of the previous point.
                    # This makes for smooth, continuous paths.
                    if len(self._points) > 0:
                        prev = self._points[-1]
                        rx, ry = self.reflect(prev.x, prev.y, prev.ctrl2.x, prev.ctrl2.y)
                        self.new.ctrl1 = Point(rx, ry)
                    self._points.append(self.new)
                else:
                    # Illustrator-like behavior:
                    # when the handle is dragged downwards,
                    # the path bulges upwards.
                    rx, ry = self.reflect(self.new.x, self.new.y, x, y)
                    self.new.ctrl2 = Point(rx, ry)
            
            # Edit mode
            elif self.new == None:
            
                pt = self._points[self.edit]
            
                # The user is pressing the mouse on a point,
                # enter drag-point mode.
                if self.overlap(pt.x, pt.y, x, y) \
                and not self.drag_handle1 \
                and not self.drag_handle2 \
                and not self.new != None:
                    self.drag_point = True
                    self.drag_handle1 = False
                    self.drag_handle2 = False

                # The user is pressing the mouse on a point's handle,
                # enter drag-handle mode.
                if self.overlap(pt.ctrl1.x, pt.ctrl1.y, x, y) \
                and pt.cmd == CURVETO \
                and not self.drag_point \
                and not self.drag_handle2:
                    self.drag_point = False
                    self.drag_handle1 = True
                    self.drag_handle2 = False
                if self.overlap(pt.ctrl2.x, pt.ctrl2.y, x, y) \
                and pt.cmd == CURVETO \
                and not self.drag_point \
                and not self.drag_handle1:
                    self.drag_point = False
                    self.drag_handle1 = False
                    self.drag_handle2 = True
                
                # In drag-point mode,
                # the point is located at the mouse coordinates.
                # The handles move relatively to the new location
                # (e.g. they are retained, the path does not distort).
                # Modify the ctrl1 handle of the next point as well.
                if self.drag_point == True:
                    dx = x - pt.x
                    dy = y - pt.y
                    pt.x = x
                    pt.y = y
                    pt.ctrl2.x += dx
                    pt.ctrl2.y += dy
                    if self.edit < len(self._points)-1:
                        rx, ry = self.reflect(pt.x, pt.y, x, y)
                        next = self._points[self.edit+1]
                        next.ctrl1.x += dx
                        next.ctrl1.y += dy

                # In drag-handle mode,
                # set the path's handle to the mouse location.
                # Rotate the handle of the next or previous point
                # to keep paths smooth - unless the user is pressing "x".
                if self.drag_handle1 == True:
                    pt.ctrl1 = Point(x, y)
                    if self.edit > 0 \
                    and self.last_key != "x":
                        prev = self._points[self.edit-1]
                        d = self.distance(prev.x, prev.y, prev.ctrl2.x, prev.ctrl2.y)
                        a = self.angle(prev.x, prev.y, pt.ctrl1.x, pt.ctrl1.y)
                        prev.ctrl2 = self.coordinates(prev.x, prev.y, d, a+180)                        
                if self.drag_handle2 == True:   
                    pt.ctrl2 = Point(x, y)
                    if self.edit < len(self._points)-1 \
                    and self.last_key != "x":
                        next = self._points[self.edit+1]
                        d = self.distance(pt.x, pt.y, next.ctrl1.x, next.ctrl1.y)
                        a = self.angle(pt.x, pt.y, pt.ctrl2.x, pt.ctrl2.y)
                        next.ctrl1 = self.coordinates(pt.x, pt.y, d, a+180)
        
        elif not self.freehand:
            
            # The mouse button is released
            # so we are not dragging anything around.
            self.new = None
            self.drag_point = False
            self.drag_handle1 = False
            self.drag_handle2 = False
            
            # The delete button for a point was clicked.
            if self.delete != None and len(self._points) > 0:
                i = self.delete
                cmd = self._points[i].cmd
                del self._points[i]
                if 0 < i < len(self._points):
                    prev = self._points[i-1]
                    rx, ry = self.reflect(prev.x, prev.y, prev.ctrl2.x, prev.ctrl2.y)
                    self._points[i].ctrl1 = Point(rx, ry)
                # Also delete all the freehand points
                # prior to this point.
                start_i = i
                while i > 1:
                    i -= 1
                    pt = self._points[i]
                    if pt.freehand:
                        del self._points[i]
                    elif i < start_i-1 and pt.freehand == False:
                        if pt.cmd == MOVETO:
                            del self._points[i]
                        break
                # When you delete a MOVETO point,
                # the last moveto (the one where the dashed line points to)
                # needs to be updated.
                if len(self._points) > 0 \
                and (cmd == MOVETO or i == 0):
                    self.last_moveto = self._points[0]
                    for pt in self._points:
                        if pt.cmd == MOVETO:
                            self.last_moveto = pt
                self.delete = None
                self.edit = None

            # The moveto button for the last point
            # in the path was clicked.
            elif isinstance(self.moveto, int):
                self.moveto = True
                self.edit = None
            
            # We are not editing a node and
            # the mouse is hovering over the path outline stroke:
            # it is possible to insert a point here.
            elif self.edit == None \
            and self.contains_point(x, y, d=2):
                self.insert = True
            else:
                self.insert = False
            
            # Commit insert of new point.
            if self.inserting \
            and self.contains_point(x, y, d=2): 
                self.insert_point(x, y)
                self.insert = False
            self.inserting = False
            
            # No modifications are being made right now
            # and the SVG file needs to be updated.
            if self._dirty == True:
                self.export_svg()
                self._dirty = False
        
        # Keyboard interaction.
        if _ctx._ns["keydown"]:
            self.last_key = _ctx._ns["key"]
            self.last_keycode = _ctx._ns["keycode"]
        if not _ctx._ns["keydown"] and self.last_key != None:
            # If the TAB-key is pressed,
            # switch the magnetic grid either on or off.
            if self.last_keycode == KEY_TAB:
                self.show_grid = not self.show_grid
            # When "f" is pressed, switch freehand mode.
            if self.last_key == "f":
                self.edit = None
                self.freehand = not self.freehand
                if self.freehand:
                    self.msg = "freehand"
                else:
                    self.msg = "curves"
            # When ESC is pressed exit edit mode.
            if self.last_keycode == KEY_ESC:
                self.edit = None
            # When BACKSPACE is pressed, delete current point.
            if self.last_keycode == _ctx.KEY_BACKSPACE \
            and self.edit != None:
                self.delete = self.edit
            self.last_key = None
            self.last_code = None
        
        # Using the keypad you can scroll the screen.
        if _ctx._ns["keydown"]:
            dx = 0
            dy = 0
            keycode = _ctx._ns["keycode"]
            if keycode == _ctx.KEY_LEFT:
                dx = -10
            elif keycode == _ctx.KEY_RIGHT:
                dx = 10
            if keycode == _ctx.KEY_UP:
                dy = -10
            elif keycode == _ctx.KEY_DOWN:
                dy = 10
            if dx != 0 or dy != 0:
                for pt in self._points:
                    pt.x += dx
                    pt.y += dy
                    pt.ctrl1.x += dx
                    pt.ctrl1.y += dy
                    pt.ctrl2.x += dx
                    pt.ctrl2.y += dy