def add_program_dir(self, directory):
        """Hack in program directory"""
        dirs = list(self.PROGRAM_DIRS)
        dirs.append(directory)
        self.PROGRAM_DIRS = dirs