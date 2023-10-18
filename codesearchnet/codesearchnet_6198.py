def parse_if_header_dict(environ):
    """Parse HTTP_IF header into a dictionary and lists, and cache the result.

    @see http://www.webdav.org/specs/rfc4918.html#HEADER_If
    """
    if "wsgidav.conditions.if" in environ:
        return

    if "HTTP_IF" not in environ:
        environ["wsgidav.conditions.if"] = None
        environ["wsgidav.ifLockTokenList"] = []
        return

    iftext = environ["HTTP_IF"].strip()
    if not iftext.startswith("<"):
        iftext = "<*>" + iftext

    ifDict = dict([])
    ifLockList = []

    resource1 = "*"
    for (tmpURLVar, URLVar, _tmpContentVar, contentVar) in reIfSeparator.findall(
        iftext
    ):
        if tmpURLVar != "":
            resource1 = URLVar
        else:
            listTagContents = []
            testflag = True
            for listitem in reIfTagListContents.findall(contentVar):
                if listitem.upper() != "NOT":
                    if listitem.startswith("["):
                        listTagContents.append(
                            (testflag, "entity", listitem.strip('"[]'))
                        )
                    else:
                        listTagContents.append(
                            (testflag, "locktoken", listitem.strip("<>"))
                        )
                        ifLockList.append(listitem.strip("<>"))
                testflag = listitem.upper() != "NOT"

            if resource1 in ifDict:
                listTag = ifDict[resource1]
            else:
                listTag = []
                ifDict[resource1] = listTag
            listTag.append(listTagContents)

    environ["wsgidav.conditions.if"] = ifDict
    environ["wsgidav.ifLockTokenList"] = ifLockList
    _logger.debug("parse_if_header_dict\n{}".format(pformat(ifDict)))
    return