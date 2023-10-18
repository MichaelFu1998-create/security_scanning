def add_texture_dir(self, directory):
        """Hack in texture directory"""
        dirs = list(self.TEXTURE_DIRS)
        dirs.append(directory)
        self.TEXTURE_DIRS = dirs