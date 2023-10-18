def _setup_launch(self):
        """
        Method to be used by all launchers that prepares the root
        directory and generate basic launch information for command
        templates to use (including a registered timestamp).
        """
        self.root_directory = self.get_root_directory()
        if not os.path.isdir(self.root_directory):
            os.makedirs(self.root_directory)

        platform_dict = {}
        python_version = (platform.python_implementation()
                          + platform.python_version())
        platform_dict['platform']       = platform.platform()
        platform_dict['python_version'] = python_version
        platform_dict['lancet_version'] = str(lancet_version)

        return {'root_directory':    self.root_directory,
                'batch_name':        self.batch_name,
                'batch_tag':         self.tag,
                'batch_description': self.description,
                'launcher':          repr(self),
                'platform' :         platform_dict,
                'timestamp':         self.timestamp,
                'timestamp_format':  self.timestamp_format,
                'varying_keys':      self.args.varying_keys,
                'constant_keys':     self.args.constant_keys,
                'constant_items':    self.args.constant_items}