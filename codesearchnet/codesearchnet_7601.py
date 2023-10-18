def save_file(self):
        """Saves the notebook to a file"""
        with open(self.write_file, 'w') as out_nb:
            json.dump(self.work_notebook, out_nb, indent=2)