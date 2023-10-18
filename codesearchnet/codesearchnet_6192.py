def add_property_response(multistatusEL, href, propList):
    """Append <response> element to <multistatus> element.

    <prop> node depends on the value type:
      - str or unicode: add element with this content
      - None: add an empty element
      - etree.Element: add XML element as child
      - DAVError: add an empty element to an own <propstatus> for this status code

    @param multistatusEL: etree.Element
    @param href: global URL of the resource, e.g. 'http://server:port/path'.
    @param propList: list of 2-tuples (name, value)
    """
    # Split propList by status code and build a unique list of namespaces
    nsCount = 1
    nsDict = {}
    nsMap = {}
    propDict = {}

    for name, value in propList:
        status = "200 OK"
        if isinstance(value, DAVError):
            status = get_http_status_string(value)
            # Always generate *empty* elements for props with error status
            value = None

        # Collect namespaces, so we can declare them in the <response> for
        # compacter output
        ns, _ = split_namespace(name)
        if ns != "DAV:" and ns not in nsDict and ns != "":
            nsDict[ns] = True
            nsMap["NS{}".format(nsCount)] = ns
            nsCount += 1

        propDict.setdefault(status, []).append((name, value))

    # <response>
    responseEL = make_sub_element(multistatusEL, "{DAV:}response", nsmap=nsMap)

    #    log("href value:{}".format(string_repr(href)))
    #    etree.SubElement(responseEL, "{DAV:}href").text = toUnicode(href)
    etree.SubElement(responseEL, "{DAV:}href").text = href
    #    etree.SubElement(responseEL, "{DAV:}href").text = compat.quote(href, safe="/" + "!*'(),"
    #       + "$-_|.")

    # One <propstat> per status code
    for status in propDict:
        propstatEL = etree.SubElement(responseEL, "{DAV:}propstat")
        # List of <prop>
        propEL = etree.SubElement(propstatEL, "{DAV:}prop")
        for name, value in propDict[status]:
            if value is None:
                etree.SubElement(propEL, name)
            elif is_etree_element(value):
                propEL.append(value)
            else:
                # value must be string or unicode
                #                log("{} value:{}".format(name, string_repr(value)))
                #                etree.SubElement(propEL, name).text = value
                etree.SubElement(propEL, name).text = to_unicode_safe(value)
        # <status>
        etree.SubElement(propstatEL, "{DAV:}status").text = "HTTP/1.1 {}".format(status)