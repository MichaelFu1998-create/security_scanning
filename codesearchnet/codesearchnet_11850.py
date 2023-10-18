def fake(self, components=None):#, set_satchels=None):
        """
        Update the thumbprint on the remote server but execute no satchel configurators.

        components = A comma-delimited list of satchel names to limit the fake deployment to.
        set_satchels = A semi-colon delimited list of key-value pairs to set in satchels before recording a fake deployment.
        """

        self.init()

        # In cases where we only want to fake deployment of a specific satchel, then simply copy the last thumbprint and overwrite with a subset
        # of the current thumbprint filtered by our target components.
        if components:
            current_tp = self.get_previous_thumbprint() or {}
            current_tp.update(self.get_current_thumbprint(components=components) or {})
        else:
            current_tp = self.get_current_thumbprint(components=components) or {}

        tp_text = yaml.dump(current_tp)
        r = self.local_renderer
        r.upload_content(content=tp_text, fn=self.manifest_filename)

        # Ensure all cached manifests are cleared, so they reflect the newly deployed changes.
        self.reset_all_satchels()