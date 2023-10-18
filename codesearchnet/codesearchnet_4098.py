def keywords(self):
        '''Generator which returns all keywords in the suite'''
        for table in self.tables:
            if isinstance(table, KeywordTable):
                for keyword in table.keywords:
                    yield keyword