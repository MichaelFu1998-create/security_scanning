def as_dict(self):
        """Return a dict that represents the DayOneEntry"""
        entry_dict = {}
        entry_dict['UUID'] = self.uuid
        entry_dict['Creation Date'] = self.time
        entry_dict['Time Zone'] = self.tz
        if self.tags:
            entry_dict['Tags'] = self.tags
        entry_dict['Entry Text'] = self.text
        entry_dict['Starred'] = self.starred
        entry_dict['Location'] = self.location
        return entry_dict