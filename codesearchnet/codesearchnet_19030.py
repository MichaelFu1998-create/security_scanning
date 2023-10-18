def verify(xml, stream):
    """
    Verify the signaure of an XML document with the given certificate.
    Returns `True` if the document is signed with a valid signature.
    Returns `False` if the document is not signed or if the signature is
    invalid.

    :param lxml.etree._Element xml: The document to sign
    :param file stream: The private key to sign the document with

    :rtype: Boolean
    """
    # Import xmlsec here to delay initializing the C library in
    # case we don't need it.
    import xmlsec

    # Find the <Signature/> node.
    signature_node = xmlsec.tree.find_node(xml, xmlsec.Node.SIGNATURE)
    if signature_node is None:
        # No `signature` node found; we cannot verify
        return False

    # Create a digital signature context (no key manager is needed).
    ctx = xmlsec.SignatureContext()

    # Register <Response/> and <Assertion/>
    ctx.register_id(xml)
    for assertion in xml.xpath("//*[local-name()='Assertion']"):
        ctx.register_id(assertion)

    # Load the public key.
    key = None
    for fmt in [
            xmlsec.KeyFormat.PEM,
            xmlsec.KeyFormat.CERT_PEM]:
        stream.seek(0)
        try:
            key = xmlsec.Key.from_memory(stream, fmt)
            break
        except ValueError:  
            # xmlsec now throws when it can't load the key
            pass

    # Set the key on the context.
    ctx.key = key

    # Verify the signature.
    try:
        ctx.verify(signature_node)

        return True

    except Exception:
        return False