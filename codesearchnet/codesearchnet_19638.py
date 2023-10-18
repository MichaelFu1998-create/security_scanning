def initialize(self, templates_path, global_data):
        """initialize with templates' path
        parameters
          templates_path    str    the position of templates directory
          global_data       dict   globa data can be got in any templates"""
        self.env = Environment(loader=FileSystemLoader(templates_path))
        self.env.trim_blocks = True
        self.global_data = global_data