def _verify_signature(message, signature, certs):
    """Verifies signed content using a list of certificates.

    Args:
        message: string or bytes, The message to verify.
        signature: string or bytes, The signature on the message.
        certs: iterable, certificates in PEM format.

    Raises:
        AppIdentityError: If none of the certificates can verify the message
                          against the signature.
    """
    for pem in certs:
        verifier = Verifier.from_string(pem, is_x509_cert=True)
        if verifier.verify(message, signature):
            return

    # If we have not returned, no certificate confirms the signature.
    raise AppIdentityError('Invalid token signature')