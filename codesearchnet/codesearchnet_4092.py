def RobotFactory(path, parent=None):
    '''Return an instance of SuiteFile, ResourceFile, SuiteFolder

    Exactly which is returned depends on whether it's a file or
    folder, and if a file, the contents of the file. If there is a
    testcase table, this will return an instance of SuiteFile,
    otherwise it will return an instance of ResourceFile.
    '''

    if os.path.isdir(path):
        return SuiteFolder(path, parent)

    else:
        rf = RobotFile(path, parent)

        for table in rf.tables:
            if isinstance(table, TestcaseTable):
                rf.__class__ = SuiteFile
                return rf

        rf.__class__ = ResourceFile
        return rf