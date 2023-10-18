def sendToLogbook(self, fileName, logType, location=None):
        '''Process log information and push to selected logbooks.'''
        import subprocess
        
        success = True
        if logType == "MCC":
            fileString = ""
            if not self.imagePixmap.isNull():
                fileString = fileName + "." + self.imageType
        
            logcmd = "xml2elog " + fileName + ".xml " + fileString
            process = subprocess.Popen(logcmd, shell=True)
            process.wait()
            if process.returncode != 0:
                success = False
        else:
            from shutil import copy

            path = "/u1/" + location.lower() + "/physics/logbook/data/"  # Prod path
            # path = "/home/softegr/alverson/log_test/"  # Dev path
            try:
                if not self.imagePixmap.isNull():
                    copy(fileName + ".png", path)
                    if self.imageType == "png":
                        copy(fileName + ".ps", path)
                    else:
                        copy(fileName + "." + self.imageType, path)
            
                # Copy .xml file last to ensure images will be picked up by cron job
                # print("Copying file " + fileName + " to path " + path)
                copy(fileName + ".xml", path)
            except IOError as error:
                print(error)
                success = False
            
        return success