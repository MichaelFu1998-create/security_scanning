def _find_last_of(self, path, finders):
        """Find the last occurance of the file in finders"""
        found_path = None
        for finder in finders:
            result = finder.find(path)
            if result:
                found_path = result

        return found_path