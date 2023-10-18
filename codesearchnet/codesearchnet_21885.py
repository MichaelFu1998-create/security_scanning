def save(self):
        '''Save the environment cache to disk.'''

        env_data = [dict(name=env.name, root=env.path) for env in self]
        encode = yaml.safe_dump(env_data, default_flow_style=False)

        with open(self.path, 'w') as f:
            f.write(encode)