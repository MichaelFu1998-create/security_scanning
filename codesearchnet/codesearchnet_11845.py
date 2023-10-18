def manifest_filename(self):
        """
        Returns the path to the manifest file.
        """
        r = self.local_renderer
        tp_fn = r.format(r.env.data_dir + '/manifest.yaml')
        return tp_fn