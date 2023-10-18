def removeLogbooks(self, type=None, logs=[]):
        '''Remove unwanted logbooks from list.'''
        if type is not None and type in self.logList:
            if len(logs) == 0 or logs == "All":
                del self.logList[type]
            else:
                for logbook in logs:
                    if logbook in self.logList[type]:
                        self.logList[type].remove(logbook)
            
            self.changeLogType()