def save(self, entry, with_location=True, debug=False):
        """Saves a DayOneEntry as a plist"""
        entry_dict = {}
        if isinstance(entry, DayOneEntry):
            # Get a dict of the DayOneEntry
            entry_dict = entry.as_dict()
        else:
            entry_dict = entry
        
        # Set the UUID
        entry_dict['UUID'] = uuid.uuid4().get_hex()
        if with_location and not entry_dict['Location']:
            entry_dict['Location'] = self.get_location()


        # Do we have everything needed?
        if not all ((entry_dict['UUID'], entry_dict['Time Zone'],
                     entry_dict['Entry Text'])):
            print "You must provide: Time zone, UUID, Creation Date, Entry Text"
            return False

        if debug is False:
            file_path = self._file_path(entry_dict['UUID'])
            plistlib.writePlist(entry_dict, file_path)
        else:
            plist = plistlib.writePlistToString(entry_dict)
            print plist

        return True