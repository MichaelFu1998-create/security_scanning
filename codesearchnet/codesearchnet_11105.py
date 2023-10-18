def get_template_dir(self):
        """Returns the absolute path to template directory"""
        directory = os.path.dirname(os.path.abspath(__file__))
        directory = os.path.dirname(os.path.dirname(directory))
        directory = os.path.join(directory, 'project_template')
        return directory