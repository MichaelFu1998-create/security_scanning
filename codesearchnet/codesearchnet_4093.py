def walk(self, *types):
        '''
        Iterator which visits all suites and suite files,
        yielding test cases and keywords
        '''
        requested = types if len(types) > 0 else [SuiteFile, ResourceFile, SuiteFolder, Testcase, Keyword]

        for thing in self.robot_files:
            if thing.__class__ in requested:
                yield thing
            if isinstance(thing, SuiteFolder):
                for child in thing.walk():
                    if child.__class__ in requested:
                        yield child
            else:
                for child in thing.walk(*types):
                    yield child