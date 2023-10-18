def removeLayout(self, layout):
        '''Iteratively remove graphical objects from layout.'''
        for cnt in reversed(range(layout.count())):
            item = layout.takeAt(cnt)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                '''If sublayout encountered, iterate recursively.'''
                self.removeLayout(item.layout())