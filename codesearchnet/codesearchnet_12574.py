def add_record_check(self, actions, table, func):
        # emitted after query
        # table: 'table_name'
        # column: ('table_name', 'column_name')
        assert isinstance(table, str), '`table` must be table name'
        for i in actions:
            assert i not in (A.QUERY, A.CREATE), "meaningless action check with record: [%s]" % i

        self.record_checks.append([table, actions, func])

        """def func(ability, user, action, record: DataRecord, available_columns: list):
            pass
        """