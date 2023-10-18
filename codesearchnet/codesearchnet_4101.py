def variables(self):
        '''Generator which returns all of the statements in all of the variables tables'''
        for table in self.tables:
            if isinstance(table, VariableTable):
                # FIXME: settings have statements, variables have rows WTF? :-(
                for statement in table.rows:
                    if statement[0] != "":
                        yield statement