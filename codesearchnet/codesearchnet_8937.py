def _render_files(self):
        """
        Renders additional files specified in ``self.config['files']``
        """
        output = ''
        # render files
        files = self.config.get('files', [])
        # add delimiter
        if files:
            output += '\n{0}\n\n'.format(self.FILE_SECTION_DELIMITER)
        for f in files:
            mode = f.get('mode', DEFAULT_FILE_MODE)
            # add file to output
            file_output = '# path: {0}\n'\
                          '# mode: {1}\n\n'\
                          '{2}\n\n'.format(f['path'], mode, f['contents'])
            output += file_output
        return output