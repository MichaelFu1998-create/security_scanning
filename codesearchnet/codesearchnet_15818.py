def copy_local_includes(self):
    """
    Copy local js/css includes from naarad resources to the report/resources directory
    :return: None
    """
    resource_folder = self.get_resources_location()
    for stylesheet in self.stylesheet_includes:
      if ('http' not in stylesheet) and naarad.utils.is_valid_file(os.path.join(resource_folder, stylesheet)):
        shutil.copy(os.path.join(resource_folder, stylesheet), self.resource_directory)

    for javascript in self.javascript_includes:
      if ('http' not in javascript) and naarad.utils.is_valid_file(os.path.join(resource_folder, javascript)):
        shutil.copy(os.path.join(resource_folder, javascript), self.resource_directory)

    return None