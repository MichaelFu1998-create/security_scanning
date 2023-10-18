def contents(self, f, text):
        """
        Called for each file
        Must return file content
        Can be wrapped

        :type f: static_bundle.files.StaticFileResult
        :type text: str|unicode
        :rtype: str|unicode
        """
        text += self._read(f.abs_path) + "\r\n"
        return text