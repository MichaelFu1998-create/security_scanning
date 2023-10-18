def update(self):
        """Update the launch information -- use if additional launches were
        made.
        """
        launches = []
        for path in os.listdir(self.output_dir):
            full_path = os.path.join(self.output_dir, path)
            if os.path.isdir(full_path):
                launches.append(self._get_launch_info(full_path))
        self.launches = sorted(launches)