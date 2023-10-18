def client_file(self):
        """Specify path to the ipcontroller-client.json file.

        This file is stored in in the ipython_dir/profile folders.

        Returns :
              - str, File path to client file
        """
        return os.path.join(self.ipython_dir,
                            'profile_{0}'.format(self.profile),
                            'security/ipcontroller-client.json')