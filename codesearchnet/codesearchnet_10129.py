def _map_oids(oids):
    """
    Takes a set of unicode string OIDs and converts vendor-specific OIDs into
    generics OIDs from RFCs.

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

    :param oids:
        A set of unicode strings

    :return:
        The original set of OIDs with any mapped OIDs added
    """

    new_oids = set()
    for oid in oids:
        if oid in _oid_map:
            new_oids |= _oid_map[oid]
    return oids | new_oids