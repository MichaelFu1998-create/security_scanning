def from_ssl_socket(cls, ssl_socket):
        """Load certificate data from an SSL socket.
        """
        cert = cls()
        try:
            data = ssl_socket.getpeercert()
        except AttributeError:
            # PyPy doesn't have .getppercert
            return cert
        logger.debug("Certificate data from ssl module: {0!r}".format(data))
        if not data:
            return cert
        cert.validated = True
        cert.subject_name = data.get('subject')
        cert.alt_names = defaultdict(list)
        if 'subjectAltName' in data:
            for name, value in data['subjectAltName']:
                cert.alt_names[name].append(value)
        if 'notAfter' in data:
            tstamp = ssl.cert_time_to_seconds(data['notAfter'])
            cert.not_after = datetime.utcfromtimestamp(tstamp)
        if sys.version_info.major < 3:
            cert._decode_names() # pylint: disable=W0212
        cert.common_names = []
        if cert.subject_name:
            for part in cert.subject_name:
                for name, value in part:
                    if name == 'commonName':
                        cert.common_names.append(value)
        return cert