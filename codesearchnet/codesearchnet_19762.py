def _remove_header(self, data, options):
        '''Remove header from data'''

        version_info = self._get_version_info(options['version'])
        header_size = version_info['header_size']

        if options['flags']['timestamp']:
            header_size += version_info['timestamp_size']

        data = data[header_size:]

        return data