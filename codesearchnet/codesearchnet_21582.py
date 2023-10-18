def add_tag(self, _tags):
        """Add tag(s) to a DayOneEntry"""
        if isinstance(_tags, list):
            for t in _tags:
                self.tags.append(t)
        else:
            self.tags.append(_tags)