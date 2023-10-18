def submitEntry(self):
        """Process user inputs and subit logbook entry when user clicks Submit button"""
        
        # logType = self.logui.logType.currentText()
        mcclogs, physlogs = self.selectedLogs()
        success = True
        
        if mcclogs != []:
            if not self.acceptedUser("MCC"):
                QMessageBox().warning(self, "Invalid User", "Please enter a valid user name!")
                return
            
            fileName = self.xmlSetup("MCC", mcclogs)
            if fileName is None:
                return
            
            if not self.imagePixmap.isNull():
                self.prepareImages(fileName, "MCC")
            success = self.sendToLogbook(fileName, "MCC")
        
        if physlogs != []:
            for i in range(len(physlogs)):
                fileName = self.xmlSetup("Physics", physlogs[i])
                if fileName is None:
                    return
            
                if not self.imagePixmap.isNull():
                    self.prepareImages(fileName, "Physics")
                success_phys = self.sendToLogbook(fileName, "Physics", physlogs[i])
                success = success and success_phys
            
        self.done(success)