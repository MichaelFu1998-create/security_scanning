def count(self):
        """Count the number of elements created, modified and deleted by the
        changeset and analyses if it is a possible import, mass modification or
        a mass deletion.
        """
        xml = get_changeset(self.id)
        actions = [action.tag for action in xml.getchildren()]
        self.create = actions.count('create')
        self.modify = actions.count('modify')
        self.delete = actions.count('delete')
        self.verify_editor()

        try:
            if (self.create / len(actions) > self.percentage and
                    self.create > self.create_threshold and
                    (self.powerfull_editor or self.create > self.top_threshold)):
                self.label_suspicious('possible import')
            elif (self.modify / len(actions) > self.percentage and
                    self.modify > self.modify_threshold):
                self.label_suspicious('mass modification')
            elif ((self.delete / len(actions) > self.percentage and
                    self.delete > self.delete_threshold) or
                    self.delete > self.top_threshold):
                self.label_suspicious('mass deletion')
        except ZeroDivisionError:
            print('It seems this changeset was redacted')