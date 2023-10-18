def on_map_long_clicked(self, pos):
        """ Called when the map is clicked """
        d = self.declaration
        d.clicked({
            'click': 'long',
            'position': tuple(pos)
        })