def xmlSetup(self, logType, logList):
        """Create xml file with fields from logbook form."""
        
        from xml.etree.ElementTree import Element, SubElement, ElementTree
        from datetime import datetime
        
        curr_time = datetime.now()
        if logType == "MCC":
            # Set up xml tags
            log_entry = Element('log_entry')
            title     = SubElement(log_entry, 'title')
            program   = SubElement(log_entry, 'program')
            timestamp = SubElement(log_entry, 'timestamp')
            priority  = SubElement(log_entry, 'priority')
            os_user   = SubElement(log_entry, 'os_user')
            hostname  = SubElement(log_entry, 'hostname')
            text      = SubElement(log_entry, 'text')
            log_user  = SubElement(log_entry, 'log_user')

            # Check for multiple logbooks and parse into seperate tags
            logbook = []
            for i in range(len(logList)):
                logbook.append(SubElement(log_entry, 'logbook'))
                logbook[i].text = logList[i].lower()
                           
            # Take care of dummy, unchanging tags first
            log_entry.attrib['type'] = "LOGENTRY"
            program.text = "152"
            priority.text = "NORMAL"
            os_user.text = "nobody"
            hostname.text = "mccelog"
            text.attrib['type'] = "text/plain"
            
            # Handle attachment if image exists
            if not self.imagePixmap.isNull():
                attachment = SubElement(log_entry, 'attachment')
                attachment.attrib['name'] = "Figure 1"
                attachment.attrib['type'] = "image/" + self.imageType
                attachment.text = curr_time.strftime("%Y%m%d_%H%M%S_") + str(curr_time.microsecond) + "." + self.imageType
            
            # Set timestamp format
            timestamp.text = curr_time.strftime("%Y/%m/%d %H:%M:%S")
            
            fileName = "/tmp/" + curr_time.strftime("%Y%m%d_%H%M%S_") + str(curr_time.microsecond) + ".xml"
            
        else:  # If using Physics logbook
            timeString = curr_time.strftime("%Y-%m-%dT%H:%M:%S")
            
            # Set up xml tags
            log_entry = Element(None)
            severity  = SubElement(log_entry, 'severity')
            location  = SubElement(log_entry, 'location')
            keywords  = SubElement(log_entry, 'keywords')
            time      = SubElement(log_entry, 'time')
            isodate   = SubElement(log_entry, 'isodate')
            log_user  = SubElement(log_entry, 'author')
            category  = SubElement(log_entry, 'category')
            title     = SubElement(log_entry, 'title')
            metainfo  = SubElement(log_entry, 'metainfo')
            
            # Handle attachment if image exists
            if not self.imagePixmap.isNull():
                imageFile = SubElement(log_entry, 'link')
                imageFile.text = timeString + "-00." + self.imageType
                thumbnail = SubElement(log_entry, 'file')
                thumbnail.text = timeString + "-00.png"
                
            text      = SubElement(log_entry, 'text')  # Logbook expects Text tag to come last (for some strange reason)
            
            # Take care of dummy, unchanging tags first
            log_entry.attrib['type'] = "LOGENTRY"
            category.text = "USERLOG"
            location.text = "not set"
            severity.text = "NONE"
            keywords.text = "none"
            
            time.text = curr_time.strftime("%H:%M:%S")
            isodate.text = curr_time.strftime("%Y-%m-%d")
            
            metainfo.text = timeString + "-00.xml"
            fileName = "/tmp/" + metainfo.text
            
        # Fill in user inputs
        log_user.text = str(self.logui.userName.text())

        title.text = str(self.logui.titleEntry.text())
        if title.text == "":
            QMessageBox().warning(self, "No Title entered", "Please enter a title for the entry...")
            return None
            
        text.text = str(self.logui.textEntry.toPlainText())
        # If text field is truly empty, ElementTree leaves off tag entirely which causes logbook parser to fail
        if text.text == "":
            text.text = " "
        
        # Create xml file
        xmlFile = open(fileName, "w")
        if logType == "MCC":
            ElementTree(log_entry).write(xmlFile)
        else:
            xmlString = self.prettify(log_entry)
            xmlFile.write(xmlString)
        xmlFile.write("\n")  # Close with newline so cron job parses correctly
        xmlFile.close()
            
        return fileName.rstrip(".xml")