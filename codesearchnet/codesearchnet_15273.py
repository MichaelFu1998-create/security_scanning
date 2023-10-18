def fs_cleansed_attachments(self):
        """ returns a list of absolute paths to the cleansed attachements"""
        if exists(self.fs_cleansed_attachment_container):
            return [join(self.fs_cleansed_attachment_container, attachment)
                    for attachment in listdir(self.fs_cleansed_attachment_container)]
        else:
            return []