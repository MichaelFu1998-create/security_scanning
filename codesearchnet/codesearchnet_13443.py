def from_der_data(cls, data):
        """Decode DER-encoded certificate.

        :Parameters:
            - `data`: the encoded certificate
        :Types:
            - `data`: `bytes`

        :Return: decoded certificate data
        :Returntype: ASN1CertificateData
        """
        # pylint: disable=W0212
        logger.debug("Decoding DER certificate: {0!r}".format(data))
        if cls._cert_asn1_type is None:
            cls._cert_asn1_type = Certificate()
        cert = der_decoder.decode(data, asn1Spec = cls._cert_asn1_type)[0]
        result = cls()
        tbs_cert = cert.getComponentByName('tbsCertificate')
        subject = tbs_cert.getComponentByName('subject')
        logger.debug("Subject: {0!r}".format(subject))
        result._decode_subject(subject)
        validity = tbs_cert.getComponentByName('validity')
        result._decode_validity(validity)
        extensions = tbs_cert.getComponentByName('extensions')
        if extensions:
            for extension in extensions:
                logger.debug("Extension: {0!r}".format(extension))
                oid = extension.getComponentByName('extnID')
                logger.debug("OID: {0!r}".format(oid))
                if oid != SUBJECT_ALT_NAME_OID:
                    continue
                value = extension.getComponentByName('extnValue')
                logger.debug("Value: {0!r}".format(value))
                if isinstance(value, Any):
                    # should be OctetString, but is Any
                    # in pyasn1_modules-0.0.1a
                    value = der_decoder.decode(value,
                                                asn1Spec = OctetString())[0]
                alt_names = der_decoder.decode(value,
                                            asn1Spec = GeneralNames())[0]
                logger.debug("SubjectAltName: {0!r}".format(alt_names))
                result._decode_alt_names(alt_names)
        return result