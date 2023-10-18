def create_environment(self, env_name, version_label=None,
                           solution_stack_name=None, cname_prefix=None, description=None,
                           option_settings=None, tier_name='WebServer', tier_type='Standard', tier_version='1.1'):
        """
        Creates a new environment
        """
        out("Creating environment: " + str(env_name) + ", tier_name:" + str(tier_name) + ", tier_type:" + str(tier_type))
        self.ebs.create_environment(self.app_name, env_name,
                                    version_label=version_label,
                                    solution_stack_name=solution_stack_name,
                                    cname_prefix=cname_prefix,
                                    description=description,
                                    option_settings=option_settings,
                                    tier_type=tier_type,
                                    tier_name=tier_name,
                                    tier_version=tier_version)