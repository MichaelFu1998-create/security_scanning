def hover(self, node):
        
        """ Displays a popup when hovering over a node.
        """
        
        if self.popup == False: return
        if self.popup == True or self.popup.node != node:
            if self.popup_text.has_key(node.id):
                texts = self.popup_text[node.id]
            else:
                texts = None
            self.popup = popup(self._ctx, node, texts)
        self.popup.draw()