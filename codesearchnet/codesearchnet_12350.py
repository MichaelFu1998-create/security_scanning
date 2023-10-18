def on_map_clicked(self, pos):
        """ Called when the map is clicked """
        d = self.declaration
        d.clicked({
            'click': 'short',
            'position': tuple(pos)
        })