def acceptedUser(self, logType):
        '''Verify enetered user name is on accepted MCC logbook list.'''
        from urllib2 import urlopen, URLError, HTTPError
        import json
        
        isApproved = False
        
        userName = str(self.logui.userName.text())
        if userName == "":
            return False  # Must have a user name to submit entry
        
        if logType == "MCC":
            networkFault = False
            data = []
            log_url = "https://mccelog.slac.stanford.edu/elog/dev/mgibbs/dev_json_user_list.php/?username=" + userName
            try:
                data = urlopen(log_url, None, 5).read()
                data = json.loads(data)
            except URLError as error:
                print("URLError: " + str(error.reason))
                networkFault = True
            except HTTPError as error:
                print("HTTPError: " + str(error.reason))
                networkFault = True
            
            # If network fails, ask user to verify
            if networkFault:
                msgBox = QMessageBox()
                msgBox.setText("Cannot connect to MCC Log Server!")
                msgBox.setInformativeText("Use entered User name anyway?")
                msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msgBox.setDefaultButton(QMessageBox.Ok)
                if msgBox.exec_() == QMessageBox.Ok:
                    isApproved = True
            
            if data != [] and (data is not None):
                isApproved = True
        else:
            isApproved = True
        return isApproved