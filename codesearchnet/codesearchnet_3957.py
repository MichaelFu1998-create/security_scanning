def check_R_package(self, package):
        """Execute a subprocess to check the package's availability.

        Args:
            package (str): Name of the package to be tested.

        Returns:
            bool: `True` if the package is available, `False` otherwise
        """
        test_package = not bool(launch_R_script("{}/R_templates/test_import.R".format(os.path.dirname(os.path.realpath(__file__))),                                      {"{package}": package}, verbose=True))
        return test_package