def has_tag(self, model):
        """Does the given port have this tag?"""
        for tag in model.tags:
            if self.is_tag(tag):
                return True
        return False