def write_directory(self, directory: str) -> bool:
        """Write a BEL namespace for identifiers, names, name hash, and mappings to the given directory."""
        current_md5_hash = self.get_namespace_hash()
        md5_hash_path = os.path.join(directory, f'{self.module_name}.belns.md5')

        if not os.path.exists(md5_hash_path):
            old_md5_hash = None
        else:
            with open(md5_hash_path) as file:
                old_md5_hash = file.read().strip()

        if old_md5_hash == current_md5_hash:
            return False

        with open(os.path.join(directory, f'{self.module_name}.belns'), 'w') as file:
            self.write_bel_namespace(file, use_names=False)

        with open(md5_hash_path, 'w') as file:
            print(current_md5_hash, file=file)

        if self.has_names:
            with open(os.path.join(directory, f'{self.module_name}-names.belns'), 'w') as file:
                self.write_bel_namespace(file, use_names=True)

            with open(os.path.join(directory, f'{self.module_name}.belns.mapping'), 'w') as file:
                self.write_bel_namespace_mappings(file, desc='writing mapping')

        return True