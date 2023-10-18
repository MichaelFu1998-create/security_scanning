def _headers(self, name, is_file=False):
        """ Returns the header of the encoding of this parameter.
        
        Args:
            name (str): Field name
        
        Kwargs:
            is_file (bool): If true, this is a file field
        
        Returns:
            array. Headers
        """
        value = self._files[name] if is_file else self._data[name]
        _boundary = self.boundary.encode("utf-8") if isinstance(self.boundary, unicode) else urllib.quote_plus(self.boundary)
   
        headers = ["--%s" % _boundary]

        if is_file:
            disposition = 'form-data; name="%s"; filename="%s"' % (name, os.path.basename(value))
        else:
            disposition = 'form-data; name="%s"' % name

        headers.append("Content-Disposition: %s" % disposition)

        if is_file:
            file_type = self._file_type(name)
        else:
            file_type = "text/plain; charset=utf-8"

        headers.append("Content-Type: %s" % file_type)

        if is_file:
            headers.append("Content-Length: %i" % self._file_size(name))
        else:
            headers.append("Content-Length: %i" % len(value))

        headers.append("")
        headers.append("")

        return "\r\n".join(headers)