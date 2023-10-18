def with_revision(self, label, number):
        """
        Returns a Tag with a given revision
        """
        t = self.clone()
        t.revision = Revision(label, number)
        return t