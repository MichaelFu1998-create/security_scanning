def initial_sanity_check(self):
        """Checks if we can create the project"""
        # Check for python module collision
        self.try_import(self.project_name)

        # Is the name a valid identifier?
        self.validate_name(self.project_name)

        # Make sure we don't mess with existing directories
        if os.path.exists(self.project_name):
            print("Directory {} already exist. Aborting.".format(self.project_name))
            return False

        if os.path.exists('manage.py'):
            print("A manage.py file already exist in the current directory. Aborting.")
            return False

        return True