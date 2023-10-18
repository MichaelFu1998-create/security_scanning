def dump(self):
        '''Regurgitate the tables and rows'''
        for table in self.tables:
            print("*** %s ***" % table.name)
            table.dump()