def get_request_subfields(root):
    """Build a basic 035 subfield with basic information from the OAI-PMH request.

    :param root: ElementTree root node

    :return: list of subfield tuples [(..),(..)]
    """
    request = root.find('request')
    responsedate = root.find('responseDate')

    subs = [("9", request.text),
            ("h", responsedate.text),
            ("m", request.attrib["metadataPrefix"])]
    return subs