def add_data_dir(self, directory):
        """Hack in a data directory"""
        dirs = list(self.DATA_DIRS)
        dirs.append(directory)
        self.DATA_DIRS = dirs