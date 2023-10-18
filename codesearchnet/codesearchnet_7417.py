def upload_attachments(self, attachments, parentid=None, basedir=None):
        """Upload files to the already created (but never uploaded) attachments"""
        return Zupload(self, attachments, parentid, basedir=basedir).upload()