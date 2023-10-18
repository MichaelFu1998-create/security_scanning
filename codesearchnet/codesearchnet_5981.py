def _get_base(server_certificate, **conn):
    """Fetch the base IAM Server Certificate."""
    server_certificate['_version'] = 1

    # Get the initial cert details:
    cert_details = get_server_certificate_api(server_certificate['ServerCertificateName'], **conn)

    if cert_details:
        server_certificate.update(cert_details['ServerCertificateMetadata'])
        server_certificate['CertificateBody'] = cert_details['CertificateBody']
        server_certificate['CertificateChain'] = cert_details.get('CertificateChain', None)

        # Cast dates from a datetime to something JSON serializable.
        server_certificate['UploadDate'] = get_iso_string(server_certificate['UploadDate'])
        server_certificate['Expiration'] = get_iso_string(server_certificate['Expiration'])

    return server_certificate