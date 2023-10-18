def do_PROPFIND(self, environ, start_response):
        """
        TODO: does not yet support If and If HTTP Conditions
        @see http://www.webdav.org/specs/rfc4918.html#METHOD_PROPFIND
        """
        path = environ["PATH_INFO"]
        res = self._davProvider.get_resource_inst(path, environ)

        # RFC: By default, the PROPFIND method without a Depth header MUST act
        # as if a "Depth: infinity" header was included.
        environ.setdefault("HTTP_DEPTH", "infinity")
        if not environ["HTTP_DEPTH"] in ("0", "1", "infinity"):
            self._fail(
                HTTP_BAD_REQUEST,
                "Invalid Depth header: '{}'.".format(environ["HTTP_DEPTH"]),
            )

        if environ["HTTP_DEPTH"] == "infinity" and not self.allow_propfind_infinite:
            self._fail(
                HTTP_FORBIDDEN,
                "PROPFIND 'infinite' was disabled for security reasons.",
                err_condition=PRECONDITION_CODE_PropfindFiniteDepth,
            )

        if res is None:
            self._fail(HTTP_NOT_FOUND)

        if environ.get("wsgidav.debug_break"):
            pass  # break point

        self._evaluate_if_headers(res, environ)

        # Parse PROPFIND request
        requestEL = util.parse_xml_body(environ, allow_empty=True)
        if requestEL is None:
            # An empty PROPFIND request body MUST be treated as a request for
            # the names and values of all properties.
            requestEL = etree.XML(
                "<D:propfind xmlns:D='DAV:'><D:allprop/></D:propfind>"
            )

        if requestEL.tag != "{DAV:}propfind":
            self._fail(HTTP_BAD_REQUEST)

        propNameList = []
        propFindMode = None
        for pfnode in requestEL:
            if pfnode.tag == "{DAV:}allprop":
                if propFindMode:
                    # RFC: allprop and name are mutually exclusive
                    self._fail(HTTP_BAD_REQUEST)
                propFindMode = "allprop"
            # TODO: implement <include> option
            #            elif pfnode.tag == "{DAV:}include":
            #                if not propFindMode in (None, "allprop"):
            #                    self._fail(HTTP_BAD_REQUEST,
            #                        "<include> element is only valid with 'allprop'.")
            #                for pfpnode in pfnode:
            #                    propNameList.append(pfpnode.tag)
            elif pfnode.tag == "{DAV:}name":
                if propFindMode:  # RFC: allprop and name are mutually exclusive
                    self._fail(HTTP_BAD_REQUEST)
                propFindMode = "name"
            elif pfnode.tag == "{DAV:}prop":
                # RFC: allprop and name are mutually exclusive
                if propFindMode not in (None, "named"):
                    self._fail(HTTP_BAD_REQUEST)
                propFindMode = "named"
                for pfpnode in pfnode:
                    propNameList.append(pfpnode.tag)

        # --- Build list of resource URIs

        reslist = res.get_descendants(depth=environ["HTTP_DEPTH"], add_self=True)
        #        if environ["wsgidav.verbose"] >= 3:
        #            pprint(reslist, indent=4)

        multistatusEL = xml_tools.make_multistatus_el()
        responsedescription = []

        for child in reslist:

            if propFindMode == "allprop":
                propList = child.get_properties("allprop")
            elif propFindMode == "name":
                propList = child.get_properties("name")
            else:
                propList = child.get_properties("named", name_list=propNameList)

            href = child.get_href()
            util.add_property_response(multistatusEL, href, propList)

        if responsedescription:
            etree.SubElement(
                multistatusEL, "{DAV:}responsedescription"
            ).text = "\n".join(responsedescription)

        return util.send_multi_status_response(environ, start_response, multistatusEL)