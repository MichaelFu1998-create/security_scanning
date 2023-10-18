def _add_tc_script(self):
        """
        generates tc_script.sh and adds it to included files
        """
        # fill context
        context = dict(tc_options=self.config.get('tc_options', []))
        # import pdb; pdb.set_trace()
        contents = self._render_template('tc_script.sh', context)
        self.config.setdefault('files', [])  # file list might be empty
        # add tc_script.sh to list of included files
        self._add_unique_file({
            "path": "/tc_script.sh",
            "contents": contents,
            "mode": "755"
        })