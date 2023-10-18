def _decode_alt_names(self, alt_names):
        """Load SubjectAltName from a ASN.1 GeneralNames value.

        :Values:
            - `alt_names`: the SubjectAltNama extension value
        :Types:
            - `alt_name`: `GeneralNames`
        """
        for alt_name in alt_names:
            tname = alt_name.getName()
            comp = alt_name.getComponent()
            if tname == "dNSName":
                key = "DNS"
                value = _decode_asn1_string(comp)
            elif tname == "uniformResourceIdentifier":
                key = "URI"
                value = _decode_asn1_string(comp)
            elif tname == "otherName":
                oid = comp.getComponentByName("type-id")
                value = comp.getComponentByName("value")
                if oid == XMPPADDR_OID:
                    key = "XmppAddr"
                    value = der_decoder.decode(value,
                                            asn1Spec = UTF8String())[0]
                    value = _decode_asn1_string(value)
                elif oid == SRVNAME_OID:
                    key = "SRVName"
                    value = der_decoder.decode(value,
                                            asn1Spec = IA5String())[0]
                    value = _decode_asn1_string(value)
                else:
                    logger.debug("Unknown other name: {0}".format(oid))
                    continue
            else:
                logger.debug("Unsupported general name: {0}"
                                                        .format(tname))
                continue
            self.alt_names[key].append(value)