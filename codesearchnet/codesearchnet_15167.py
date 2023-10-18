def _process_loaded_object(self, path):
        """process the :paramref:`path`.

        :param str path: the path to load an svg from
        """
        file_name = os.path.basename(path)
        name = os.path.splitext(file_name)[0]
        with open(path) as file:
            string = file.read()
            self._instruction_type_to_file_content[name] = string