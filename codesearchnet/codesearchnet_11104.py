def create_entrypoint(self):
        """Write manage.py in the current directory"""
        with open(os.path.join(self.template_dir, 'manage.py'), 'r') as fd:
            data = fd.read().format(project_name=self.project_name)

        with open('manage.py', 'w') as fd:
            fd.write(data)

        os.chmod('manage.py', 0o777)