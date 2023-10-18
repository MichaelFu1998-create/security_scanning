def is_certificate_valid(stream, cert):
        """Default certificate verification callback for TLS connections.

        :Parameters:
            - `cert`: certificate information
        :Types:
            - `cert`: `CertificateData`

        :return: computed verification result.
        """
        try:
            logger.debug("tls_is_certificate_valid(cert = {0!r})".format(cert))
            if not cert:
                logger.warning("No TLS certificate information received.")
                return False
            if not cert.validated:
                logger.warning("TLS certificate not validated.")
                return False
            srv_type = stream.transport._dst_service # pylint: disable=W0212
            if cert.verify_server(stream.peer, srv_type):
                logger.debug(" tls: certificate valid for {0!r}"
                                                        .format(stream.peer))
                return True
            else:
                logger.debug(" tls: certificate not valid for {0!r}"
                                                        .format(stream.peer))
                return False
        except:
            logger.exception("Exception caught while checking a certificate")
            raise