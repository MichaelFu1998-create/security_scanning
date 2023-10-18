def get_abs_and_rel_paths(self, root_path, file_name, input_dir):
        """
        Return absolute and relative path for file

        :type root_path: str|unicode
        :type file_name: str|unicode
        :type input_dir: str|unicode
        :rtype: tuple

        """
        # todo: change relative path resolving [bug on duplicate dir names in path]
        relative_dir = root_path.replace(input_dir, '')
        return os.path.join(root_path, file_name), relative_dir + '/' + file_name