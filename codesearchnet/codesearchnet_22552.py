def get_files(self):
        """
        :inheritdoc
        """
        assert self.bundle, 'Cannot fetch directory name with empty bundle'
        result_files = []
        bundle_ext = self.bundle.get_extension()
        ext = "." + bundle_ext if bundle_ext else None
        if self.directory_path == "":
            root_path = self.bundle.path
        else:
            root_path = os.path.join(self.bundle.path, self.directory_path)
        for root, dirs, files in os.walk(root_path):
            for fpath in files:
                if (not ext or fpath.endswith(ext)) and (not self.exclusions or all(fpath != n for n in self.exclusions)):
                    abs_path, rel_path = self.get_abs_and_rel_paths(root, fpath, self.bundle.input_dir)
                    file_cls = self.bundle.get_file_cls()
                    result_files.append(file_cls(rel_path, abs_path))
        return result_files