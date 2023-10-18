def settings(self):
        '''Generator which returns all of the statements in all of the settings tables'''
        for table in self.tables:
            if isinstance(table, SettingTable):
                for statement in table.statements:
                    yield statement