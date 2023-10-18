def robot_files(self):
        '''Return a list of all folders, and test suite files (.txt, .robot)
        '''
        result = []
        for name in os.listdir(self.path):
            fullpath = os.path.join(self.path, name)
            if os.path.isdir(fullpath):
                result.append(RobotFactory(fullpath, parent=self))
            else:
                if ((name.endswith(".txt") or name.endswith(".robot")) and
                    (name not in ("__init__.txt", "__init__.robot"))):

                    result.append(RobotFactory(fullpath, parent=self))
        return result