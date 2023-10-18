def update(self):
    
        """ Interacts with the graph by clicking or dragging nodes.
        Hovering a node fires the callback function events.hover().
        Clicking a node fires the callback function events.click().
        """
    
        if self.mousedown:
        
            # When not pressing or dragging, check each node.
            if not self.pressed and not self.dragged:
                for n in self.graph.nodes:
                    if self.mouse in n:
                        self.pressed = n
                        break
                    
            # If a node is pressed, check if a drag is started.
            elif self.pressed and not self.mouse in self.pressed:
                self.dragged = self.pressed
                self.pressed = None
            
            # Drag the node (right now only for springgraphs).
            elif self.dragged and self.graph.layout.type == "spring":
                self.drag(self.dragged)
                self.graph.layout.i = min(100, max(2, self.graph.layout.n-100))
    
        # Mouse is clicked on a node, fire callback.
        elif self.pressed and self.mouse in self.pressed:
            self.clicked = self.pressed
            self.pressed = None
            self.graph.layout.i = 2
            self.click(self.clicked)
    
        # Mouse up.
        else:
            self.hovered = None
            self.pressed = None
            self.dragged = None
        
            # Hovering over a node?
            for n in self.graph.nodes:
                if self.mouse in n:
                    self.hovered = n
                    self.hover(n)
                    break