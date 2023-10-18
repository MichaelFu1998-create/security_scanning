def environment_name_for_cname(self, env_cname):
        """
        Returns an environment name for the given cname
        """
        envs = self.get_environments()
        for env in envs:
            if env['Status'] != 'Terminated' \
                and 'CNAME' in env \
                and env['CNAME'] \
                and env['CNAME'].lower().startswith(env_cname.lower() + '.'):
                return env['EnvironmentName']
        return None