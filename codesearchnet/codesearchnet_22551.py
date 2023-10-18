def get_files(self):
        """
        :inheritdoc
        """
        assert self.bundle, 'Cannot fetch file name with empty bundle'
        abs_path, rel_path = self.get_abs_and_rel_paths(self.bundle.path, self.file_path, self.bundle.input_dir)
        file_cls = self.bundle.get_file_cls()
        return [file_cls(rel_path, abs_path)]