def addLogbooks(self, type=None, logs=[], default=""):
        '''Add or change list of logbooks.'''
        if type is not None and len(logs) != 0:
            if type in self.logList:
                for logbook in logs:
                    if logbook not in self.logList.get(type)[0]:
                        # print("Adding log " + " to " + type + " log type.")
                        self.logList.get(type)[0].append(logbook)
            else:
                # print("Adding log type: " + type)
                self.logList[type] = []
                self.logList[type].append(logs)
            
            # If default given, auto-select upon menu creation
            if len(self.logList[type]) > 1 and default != "":
                self.logList.get(type)[1] == default
            else:
                self.logList.get(type).append(default)
            
            self.logType.clear()
            self.logType.addItems(list(self.logList.keys()))
            self.changeLogType()