def _get_absolute_path(self, relative_path):
        '''str: Return the received relative_path joined with the base path
        (None if there were some error).'''
        try:
            return os.path.join(self.base_path, relative_path)
        except (AttributeError, TypeError):
            pass