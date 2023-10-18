def _add_header(self, data, options):
        '''Add header to data'''

        # pylint: disable=W0142

        version_info = self._get_version_info(options['version'])

        flags = options['flags']

        header_flags = dict(
            (i, str(int(j))) for i, j in options['flags'].iteritems())
        header_flags = ''.join(version_info['flags'](**header_flags))
        header_flags = int(header_flags, 2)
        options['flags'] = header_flags

        header = version_info['header']
        header = header(**options)
        header = pack(version_info['header_format'], *header)

        if 'timestamp' in flags and flags['timestamp']:
            timestamp = long(time())
            timestamp = pack(version_info['timestamp_format'], timestamp)
            header = header + timestamp

        return header + data