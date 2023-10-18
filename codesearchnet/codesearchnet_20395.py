def reverse(self):
        """ Restore content in target file to be before any changes """
        if self._original_target_content:
            with open(self.target, 'w') as fp:
                fp.write(self._original_target_content)