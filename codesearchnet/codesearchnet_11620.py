def ignores(self, path):
        ''' Test if this module ignores the file at "path", which must be a
            path relative to the root of the module.

            If a file is within a directory that is ignored, the file is also
            ignored.
        '''
        test_path = PurePath('/', path)

        # also check any parent directories of this path against the ignore
        # patterns:
        test_paths = tuple([test_path] + list(test_path.parents))

        for exp in self.ignore_patterns:
            for tp in test_paths:
                if tp.match(exp):
                    logger.debug('"%s" ignored ("%s" matched "%s")', path, tp, exp)
                    return True
        return False