def getToolchainFiles(self):
        ''' return a list of toolchain file paths in override order (starting
            at the bottom/leaf of the hierarchy and ending at the base).
            The list is returned in the order they should be included
            (most-derived last).
        '''
        return reversed([
            os.path.join(x.path, x.description['toolchain']) for x in self.hierarchy if 'toolchain' in x.description
        ])