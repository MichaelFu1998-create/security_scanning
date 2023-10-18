def fs_dirty_attachments(self):
        """ returns a list of absolute paths to the attachements"""
        if exists(self.fs_attachment_container):
            return [join(self.fs_attachment_container, attachment)
                    for attachment in listdir(self.fs_attachment_container)]
        else:
            return []