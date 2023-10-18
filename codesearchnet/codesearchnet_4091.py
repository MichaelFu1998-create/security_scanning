def is_comment(self):
        '''Return True if the first non-empty cell starts with "#"'''

        for cell in self[:]:
            if cell == "":
                continue

            # this is the first non-empty cell. Check whether it is
            # a comment or not.
            if cell.lstrip().startswith("#"):
                return True
            else:
                return False
        return False