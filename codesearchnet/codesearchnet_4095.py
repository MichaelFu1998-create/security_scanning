def walk(self, *types):
        '''
        Iterator which can return all test cases and/or keywords

        You can specify with objects to return as parameters; if
        no parameters are given, both tests and keywords will
        be returned.

        For example, to get only test cases, you could call it
        like this:

            robot_file = RobotFactory(...)
            for testcase in robot_file.walk(Testcase): ...

        '''
        requested = types if len(types) > 0 else [Testcase, Keyword]

        if Testcase in requested:
            for testcase in self.testcases:
                yield testcase

        if Keyword in requested:
            for keyword in self.keywords:
                yield keyword