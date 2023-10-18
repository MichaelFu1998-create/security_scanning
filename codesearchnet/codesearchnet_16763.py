def delete_application(self):
        """
        Creats an application and sets the helpers current
        app_name to the created application
        """
        out("Deleting application " + str(self.app_name))
        self.ebs.delete_application(self.app_name, terminate_env_by_force=True)