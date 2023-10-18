def type(self):
        '''Return 'suite' or 'resource' or None

        This will return 'suite' if a testcase table is found;
        It will return 'resource' if at least one robot table
        is found. If no tables are found it will return None
        '''

        robot_tables = [table for table in self.tables if not isinstance(table, UnknownTable)]
        if len(robot_tables) == 0:
            return None

        for table in self.tables:
            if isinstance(table, TestcaseTable):
                return "suite"

        return "resource"