def _decode_subject(self, subject):
        """Load data from a ASN.1 subject.
        """
        self.common_names = []
        subject_name = []
        for rdnss in subject:
            for rdns in rdnss:
                rdnss_list = []
                for nameval in rdns:
                    val_type = nameval.getComponentByName('type')
                    value = nameval.getComponentByName('value')
                    if val_type not in DN_OIDS:
                        logger.debug("OID {0} not supported".format(val_type))
                        continue
                    val_type = DN_OIDS[val_type]
                    value = der_decoder.decode(value,
                                            asn1Spec = DirectoryString())[0]
                    value = value.getComponent()
                    try:
                        value = _decode_asn1_string(value)
                    except UnicodeError:
                        logger.debug("Cannot decode value: {0!r}".format(value))
                        continue
                    if val_type == u"commonName":
                        self.common_names.append(value)
                    rdnss_list.append((val_type, value))
                subject_name.append(tuple(rdnss_list))
        self.subject_name = tuple(subject_name)