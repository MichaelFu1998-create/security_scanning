def show(self):
        '''Display menus and connect even signals.'''
        self.parent.addLayout(self._logSelectLayout)
        self.menuCount += 1
        self._connectSlots()