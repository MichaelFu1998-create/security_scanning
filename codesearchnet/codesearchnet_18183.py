def sort_pem_objects(pem_objects):
    """
    Given a list of pem objects, sort the objects into the private key, leaf
    certificate, and list of CA certificates in the trust chain. This function
    assumes that the list of pem objects will contain exactly one private key
    and exactly one leaf certificate and that only key and certificate type
    objects are provided.
    """
    keys, certs, ca_certs = [], [], []
    for pem_object in pem_objects:
        if isinstance(pem_object, pem.Key):
            keys.append(pem_object)
        else:
            # This assumes all pem objects provided are either of type pem.Key
            # or pem.Certificate. Technically, there are CSR and CRL types, but
            # we should never be passed those.
            if _is_ca(pem_object):
                ca_certs.append(pem_object)
            else:
                certs.append(pem_object)

    [key], [cert] = keys, certs
    return key, cert, ca_certs