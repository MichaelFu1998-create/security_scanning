def delete_environment(self, environment_name):
        """
        Deletes an environment
        """
        self.ebs.terminate_environment(environment_name=environment_name, terminate_resources=True)