def get_schema(self):
        '''
        Hook point for overriding how the CounterPool determines the schema
        to be used when creating a missing table.
        '''
        if not self.schema:
            raise NotImplementedError(
                'You must provide a schema value or override the get_schema method'
            )

        return self.conn.create_schema(**self.schema)