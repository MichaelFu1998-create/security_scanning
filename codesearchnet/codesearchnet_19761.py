def _read_header(self, data):
        '''Read header from data'''

        # pylint: disable=W0212

        version = self._read_version(data)
        version_info = self._get_version_info(version)
        header_data = data[:version_info['header_size']]
        header = version_info['header']
        header = header._make(
            unpack(version_info['header_format'], header_data))
        header = dict(header._asdict())

        flags = list("{0:0>8b}".format(header['flags']))
        flags = dict(version_info['flags']._make(flags)._asdict())
        flags = dict((i, bool(int(j))) for i, j in flags.iteritems())
        header['flags'] = flags

        timestamp = None
        if flags['timestamp']:
            ts_start = version_info['header_size']
            ts_end = ts_start + version_info['timestamp_size']
            timestamp_data = data[ts_start:ts_end]
            timestamp = unpack(
                version_info['timestamp_format'], timestamp_data)[0]
        header['info'] = {'timestamp': timestamp}

        return header