def _add_uninstall(self, context):
        """
        generates uninstall.sh and adds it to included files
        """
        contents = self._render_template('uninstall.sh', context)
        self.config.setdefault('files', [])  # file list might be empty
        # add uninstall.sh to list of included files
        self._add_unique_file({
            "path": "/uninstall.sh",
            "contents": contents,
            "mode": "755"
        })