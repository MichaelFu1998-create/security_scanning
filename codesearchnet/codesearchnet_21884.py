def load(self):
        '''Load the environment cache from disk.'''

        if not os.path.exists(self.path):
            return

        with open(self.path, 'r') as f:
            env_data = yaml.load(f.read())

        if env_data:
            for env in env_data:
                self.add(VirtualEnvironment(env['root']))