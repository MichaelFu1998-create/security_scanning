def free(self):
        """
        Unlink and free the XML node owned by `self`.
        """
        if not self.borrowed:
            self.xmlnode.unlinkNode()
            self.xmlnode.freeNode()
        self.xmlnode=None