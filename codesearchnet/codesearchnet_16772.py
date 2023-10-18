def deploy_version(self, environment_name, version_label):
        """
        Deploys a version to an environment
        """
        out("Deploying " + str(version_label) + " to " + str(environment_name))
        self.ebs.update_environment(environment_name=environment_name, version_label=version_label)