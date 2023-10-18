def changeLogType(self):
        '''Populate log program list to correspond with log type selection.'''
        logType = self.selectedType()
        programs = self.logList.get(logType)[0]
        default = self.logList.get(logType)[1]
        if logType in self.logList:
            self.programName.clear()
            self.programName.addItems(programs)
            self.programName.setCurrentIndex(programs.index(default))