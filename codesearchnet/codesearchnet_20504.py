def _import_config(filepath):
        """
        Imports filetree and root_path variable values from the filepath.

        :param filepath:
        :return: root_path and filetree
        """
        if not op.isfile(filepath):
            raise IOError('Data config file not found. '
                          'Got: {0}'.format(filepath))

        cfg = import_pyfile(filepath)

        if not hasattr(cfg, 'root_path'):
            raise KeyError('Config file root_path key not found.')

        if not hasattr(cfg, 'filetree'):
            raise KeyError('Config file filetree key not found.')

        return cfg.root_path, cfg.filetree