def get(self, id):
        """id or slug"""
        info = super(Images, self).get(id)
        return ImageActions(self.api, parent=self, **info)