def create_application(self, description=None):
        """
        Creats an application and sets the helpers current
        app_name to the created application
        """
        out("Creating application " + str(self.app_name))
        self.ebs.create_application(self.app_name, description=description)