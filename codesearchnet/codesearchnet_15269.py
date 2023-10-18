def size_attachments(self):
        """returns the number of bytes that the cleansed attachments take up on disk"""
        total_size = 0
        for attachment in self.fs_cleansed_attachments:
                total_size += stat(attachment).st_size
        return total_size