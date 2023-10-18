def swap_environment_cnames(self, from_env_name, to_env_name):
        """
        Swaps cnames for an environment
        """
        self.ebs.swap_environment_cnames(source_environment_name=from_env_name,
                                         destination_environment_name=to_env_name)