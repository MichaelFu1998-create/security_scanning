def replace(self, **k):
        """Note returns a new Date obj"""
        if self.date != 'infinity':
            return Date(self.date.replace(**k))
        else:
            return Date('infinity')