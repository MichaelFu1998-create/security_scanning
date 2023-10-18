def engine_file(self):
        """Specify path to the ipcontroller-engine.json file.

        This file is stored in in the ipython_dir/profile folders.

        Returns :
              - str, File path to engine file
        """
        return os.path.join(self.ipython_dir,
                            'profile_{0}'.format(self.profile),
                            'security/ipcontroller-engine.json')