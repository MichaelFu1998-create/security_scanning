def get_table(self):
        '''
        Hook point for overriding how the CounterPool transforms table_name
        into a boto DynamoDB Table object.
        '''
        if hasattr(self, '_table'):
            table = self._table
        else:
            try:
                table = self.conn.get_table(self.get_table_name())
            except boto.exception.DynamoDBResponseError:
                if self.auto_create_table:
                    table = self.create_table()
                else:
                    raise

            self._table = table

        return table