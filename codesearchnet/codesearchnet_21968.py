def addLogbook(self, physDef= "LCLS", mccDef="MCC", initialInstance=False):
        '''Add new block of logbook selection windows. Only 5 allowed.'''
        if self.logMenuCount < 5:
            self.logMenus.append(LogSelectMenu(self.logui.multiLogLayout, initialInstance))
            self.logMenus[-1].addLogbooks(self.logTypeList[1], self.physics_programs, physDef)
            self.logMenus[-1].addLogbooks(self.logTypeList[0], self.mcc_programs, mccDef)
            self.logMenus[-1].show()
            self.logMenuCount += 1
            if initialInstance:
                # Initial logbook menu can add additional menus, all others can only remove themselves.
                QObject.connect(self.logMenus[-1].logButton, SIGNAL("clicked()"), self.addLogbook)
            else:
                from functools import partial
                QObject.connect(self.logMenus[-1].logButton, SIGNAL("clicked()"), partial(self.removeLogbook, self.logMenus[-1]))