def write_config(self, initialize_indices=False):
        """
            Write the current config to disk to store them.
        """
        if not os.path.exists(self.config_dir):
            os.mkdir(self.config_dir)

        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

        if initialize_indices:
            index = self.get('jackal', 'index')
            from jackal import Host, Range, Service, User, Credential, Log
            from jackal.core import create_connection
            create_connection(self)
            Host.init(index="{}-hosts".format(index))
            Range.init(index="{}-ranges".format(index))
            Service.init(index="{}-services".format(index))
            User.init(index="{}-users".format(index))
            Credential.init(index="{}-creds".format(index))
            Log.init(index="{}-log".format(index))