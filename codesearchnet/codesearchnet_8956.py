def _add_install(self, context):
        """
        generates install.sh and adds it to included files
        """
        contents = self._render_template('install.sh', context)
        self.config.setdefault('files', [])  # file list might be empty
        # add install.sh to list of included files
        self._add_unique_file({
            "path": "/install.sh",
            "contents": contents,
            "mode": "755"
        })