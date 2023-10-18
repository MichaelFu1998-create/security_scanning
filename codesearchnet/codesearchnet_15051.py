def included(self, path, is_dir=False):
        """Check patterns in order, last match that includes or excludes `path` wins. Return `None` on undecided."""
        inclusive = None
        for pattern in self.patterns:
            if pattern.is_dir == is_dir and pattern.matches(path):
                inclusive = pattern.inclusive

        #print('+++' if inclusive else '---', path, pattern)
        return inclusive