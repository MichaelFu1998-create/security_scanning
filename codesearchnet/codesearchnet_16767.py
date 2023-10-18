def rebuild_environment(self, env_name):
        """
        Rebuilds an environment
        """
        out("Rebuilding " + str(env_name))
        self.ebs.rebuild_environment(environment_name=env_name)