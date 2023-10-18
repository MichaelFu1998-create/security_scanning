def create_table(self):
        '''
        Hook point for overriding how the CounterPool creates a new table
        in DynamooDB
        '''
        table = self.conn.create_table(
            name=self.get_table_name(),
            schema=self.get_schema(),
            read_units=self.get_read_units(),
            write_units=self.get_write_units(),
        )

        if table.status != 'ACTIVE':
            table.refresh(wait_for_active=True, retry_seconds=1)

        return table