def writeDescription(self):
        ''' Write the current (possibly modified) component description to a
            package description file in the component directory.
        '''
        ordered_json.dump(os.path.join(self.path, self.description_filename), self.description)
        if self.vcs:
            self.vcs.markForCommit(self.description_filename)