def selectedLogs(self):
        '''Return selected log books by type.'''
        mcclogs = []
        physlogs = []
        for i in range(len(self.logMenus)):
            logType = self.logMenus[i].selectedType()
            log = self.logMenus[i].selectedProgram()
            if logType == "MCC":
                if log not in mcclogs:
                    mcclogs.append(log)
            elif logType == "Physics":
                if log not in physlogs:
                    physlogs.append(log)
        return mcclogs, physlogs