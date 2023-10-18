def sha1(self):
        """SHA1 hash of the config file itself."""
        with open(self.path, 'rb') as f:
            return hashlib.sha1(f.read()).hexdigest()