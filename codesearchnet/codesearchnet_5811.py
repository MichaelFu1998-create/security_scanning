def code_challenge(verifier):
    """
    Creates a 'code_challenge' as described in section 4.2 of RFC 7636
    by taking the sha256 hash of the verifier and then urlsafe
    base64-encoding it.

    Args:
        verifier: bytestring, representing a code_verifier as generated by
            code_verifier().

    Returns:
        Bytestring, representing a urlsafe base64-encoded sha256 hash digest,
            without '=' padding.
    """
    digest = hashlib.sha256(verifier).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b'=')