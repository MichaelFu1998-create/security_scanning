def remote_file_exists(self):
        """Verify whether the file (scene) exists on AWS Storage."""
        url = join(self.base_url, 'index.html')
        return super(AWSDownloader, self).remote_file_exists(url)