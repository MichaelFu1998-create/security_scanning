def sign(xml, stream, password=None):
    """
    Sign an XML document with the given private key file. This will add a
    <Signature> element to the document.

    :param lxml.etree._Element xml: The document to sign
    :param file stream: The private key to sign the document with
    :param str password: The password used to access the private key

    :rtype: None

    Example usage:
    ::
        from saml import schema
        from lxml import etree

        document = schema.AuthenticationRequest()
        xml_document = document.serialize()
        with open('my_key_file.pem', 'r+') as stream:
            sign(xml_document, stream)

        print etree.tostring(xml_document)

    Produces the following XML document:

    .. code-block:: xml

        <samlp:AuthnRequest
            xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
            xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"
            Version="2.0" ID="_6087de0b111b44349a70ff40191a4c0c"
            IssueInstant="2015-03-16T21:06:39Z">
            <Signature xmlns="http://www.w3.org/2000/09/xmldsig#">
                <SignedInfo>
                    <CanonicalizationMethod
                        Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
                        <SignatureMethod
                            Algorithm="http://www.w3.org/2000/
                            09/xmldsig#rsa-sha1"/>
                            <Reference>
                                <Transforms>
                                    <Transform
                                        Algorithm="http://www.w3.org/2000/
                                        09/xmldsig#enveloped-signature"/>
                                </Transforms>
                                <DigestMethod
                                    Algorithm="http://www.w3.org/2000/
                                    09/xmldsig#sha1"/>
                                    <DigestValue>
                                        94O1FOjRE4JQYVDqStkYzne9StQ=
                                    </DigestValue>
                            </Reference>
                </SignedInfo>
                <SignatureValue>
                    aFYRRjtB3bDyLLJzLZmsn0K4SXmOpFYJ+8R8D31VojgiF37FOElbE56UFbm8BAjn
                    l2AixrUGXP4djxoxxnfBD/reYw5yVuIVXlMxKec784nF2V4GyrfwJOKaNmlVPkq5
                    c8SI+EkKJ02mwiail0Zvjb9FzwvlYD+osMSXvJXVqnGHQDVFlhwbBRRVB6t44/M3
                    TzC4mLSVhuvcpsm4GTQSpGkHP7HvweKN/OTc0aTy8Kh/YUrImwnUCii+J0EW4nGg
                    71eZyq/IiSPnTD09WDHsWe3g29kpicZXqrQCWeLE2zfVKtyxxs7PyEmodH19jXyz
                    wh9hQ8t6PFO47Ros5aV0bw==
                </SignatureValue>
            </Signature>
        </samlp:AuthnRequest>
    """

    # Import xmlsec here to delay initializing the C library in
    # case we don't need it.
    import xmlsec

    # Resolve the SAML/2.0 element in question.
    from saml.schema.base import _element_registry
    element = _element_registry.get(xml.tag)

    # Create a signature template for RSA-SHA1 enveloped signature.
    signature_node = xmlsec.template.create(
        xml,
        xmlsec.Transform.EXCL_C14N,
        xmlsec.Transform.RSA_SHA1)

    # Add the <ds:Signature/> node to the document.
    xml.insert(element.meta.signature_index, signature_node)

    # Add the <ds:Reference/> node to the signature template.
    ref = xmlsec.template.add_reference(
        signature_node, xmlsec.Transform.SHA1)

    # Add the enveloped transform descriptor.
    xmlsec.template.add_transform(ref, xmlsec.Transform.ENVELOPED)

    # Create a digital signature context (no key manager is needed).
    ctx = xmlsec.SignatureContext()

    # Load private key.
    key = xmlsec.Key.from_memory(stream, xmlsec.KeyFormat.PEM, password)

    # Set the key on the context.
    ctx.key = key

    # Sign the template.
    ctx.sign(signature_node)