def removeLogbook(self, menu=None):
        '''Remove logbook menu set.'''
        if self.logMenuCount > 1 and menu is not None:
            menu.removeMenu()
            self.logMenus.remove(menu)
            self.logMenuCount -= 1