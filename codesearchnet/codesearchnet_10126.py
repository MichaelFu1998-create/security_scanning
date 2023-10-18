def get_list(cache_length=24, map_vendor_oids=True, cert_callback=None):
    """
    Retrieves (and caches in memory) the list of CA certs from the OS. Includes
    trust information from the OS - purposes the certificate should be trusted
    or rejected for.

    Trust information is encoded via object identifiers (OIDs) that are sourced
    from various RFCs and vendors (Apple and Microsoft). This trust information
    augments what is in the certificate itself. Any OID that is in the set of
    trusted purposes indicates the certificate has been explicitly trusted for
    a purpose beyond the extended key purpose extension. Any OID in the reject
    set is a purpose that the certificate should not be trusted for, even if
    present in the extended key purpose extension.

    *A list of common trust OIDs can be found as part of the `KeyPurposeId()`
    class in the `asn1crypto.x509` module of the `asn1crypto` package.*

    :param cache_length:
        The number of hours to cache the CA certs in memory before they are
        refreshed

    :param map_vendor_oids:
        A bool indicating if the following mapping of OIDs should happen for
        trust information from the OS trust list:
         - 1.2.840.113635.100.1.3 (apple_ssl) -> 1.3.6.1.5.5.7.3.1 (server_auth)
         - 1.2.840.113635.100.1.3 (apple_ssl) -> 1.3.6.1.5.5.7.3.2 (client_auth)
         - 1.2.840.113635.100.1.8 (apple_smime) -> 1.3.6.1.5.5.7.3.4 (email_protection)
         - 1.2.840.113635.100.1.9 (apple_eap) -> 1.3.6.1.5.5.7.3.13 (eap_over_ppp)
         - 1.2.840.113635.100.1.9 (apple_eap) -> 1.3.6.1.5.5.7.3.14 (eap_over_lan)
         - 1.2.840.113635.100.1.11 (apple_ipsec) -> 1.3.6.1.5.5.7.3.5 (ipsec_end_system)
         - 1.2.840.113635.100.1.11 (apple_ipsec) -> 1.3.6.1.5.5.7.3.6 (ipsec_tunnel)
         - 1.2.840.113635.100.1.11 (apple_ipsec) -> 1.3.6.1.5.5.7.3.7 (ipsec_user)
         - 1.2.840.113635.100.1.11 (apple_ipsec) -> 1.3.6.1.5.5.7.3.17 (ipsec_ike)
         - 1.2.840.113635.100.1.16 (apple_code_signing) -> 1.3.6.1.5.5.7.3.3 (code_signing)
         - 1.2.840.113635.100.1.20 (apple_time_stamping) -> 1.3.6.1.5.5.7.3.8 (time_stamping)
         - 1.3.6.1.4.1.311.10.3.2 (microsoft_time_stamp_signing) -> 1.3.6.1.5.5.7.3.8 (time_stamping)

    :param cert_callback:
        A callback that is called once for each certificate in the trust store.
        It should accept two parameters: an asn1crypto.x509.Certificate object,
        and a reason. The reason will be None if the certificate is being
        exported, otherwise it will be a unicode string of the reason it won't.

    :raises:
        oscrypto.errors.CACertsError - when an error occurs exporting/locating certs

    :return:
        A (copied) list of 3-element tuples containing CA certs from the OS
        trust ilst:
         - 0: an asn1crypto.x509.Certificate object
         - 1: a set of unicode strings of OIDs of trusted purposes
         - 2: a set of unicode strings of OIDs of rejected purposes
    """

    if not _in_memory_up_to_date(cache_length):
        with memory_lock:
            if not _in_memory_up_to_date(cache_length):
                certs = []
                for cert_bytes, trust_oids, reject_oids in extract_from_system(cert_callback):
                    if map_vendor_oids:
                        trust_oids = _map_oids(trust_oids)
                        reject_oids = _map_oids(reject_oids)
                    certs.append((Certificate.load(cert_bytes), trust_oids, reject_oids))
                _module_values['certs'] = certs
                _module_values['last_update'] = time.time()

    return list(_module_values['certs'])