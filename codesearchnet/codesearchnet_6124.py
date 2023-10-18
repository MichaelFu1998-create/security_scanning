def do_PROPPATCH(self, environ, start_response):
        """Handle PROPPATCH request to set or remove a property.

        @see http://www.webdav.org/specs/rfc4918.html#METHOD_PROPPATCH
        """
        path = environ["PATH_INFO"]
        res = self._davProvider.get_resource_inst(path, environ)

        # Only accept Depth: 0 (but assume this, if omitted)
        environ.setdefault("HTTP_DEPTH", "0")
        if environ["HTTP_DEPTH"] != "0":
            self._fail(HTTP_BAD_REQUEST, "Depth must be '0'.")

        if res is None:
            self._fail(HTTP_NOT_FOUND)

        self._evaluate_if_headers(res, environ)
        self._check_write_permission(res, "0", environ)

        # Parse request
        requestEL = util.parse_xml_body(environ)

        if requestEL.tag != "{DAV:}propertyupdate":
            self._fail(HTTP_BAD_REQUEST)

        # Create a list of update request tuples: (name, value)
        propupdatelist = []

        for ppnode in requestEL:
            propupdatemethod = None
            if ppnode.tag == "{DAV:}remove":
                propupdatemethod = "remove"
            elif ppnode.tag == "{DAV:}set":
                propupdatemethod = "set"
            else:
                self._fail(
                    HTTP_BAD_REQUEST, "Unknown tag (expected 'set' or 'remove')."
                )

            for propnode in ppnode:
                if propnode.tag != "{DAV:}prop":
                    self._fail(HTTP_BAD_REQUEST, "Unknown tag (expected 'prop').")

                for propertynode in propnode:
                    propvalue = None
                    if propupdatemethod == "remove":
                        propvalue = None  # Mark as 'remove'
                        if len(propertynode) > 0:
                            # 14.23: All the XML elements in a 'prop' XML
                            # element inside of a 'remove' XML element MUST be
                            # empty
                            self._fail(
                                HTTP_BAD_REQUEST,
                                "prop element must be empty for 'remove'.",
                            )
                    else:
                        propvalue = propertynode

                    propupdatelist.append((propertynode.tag, propvalue))

        # Apply updates in SIMULATION MODE and create a result list (name,
        # result)
        successflag = True
        writeresultlist = []

        for (name, propvalue) in propupdatelist:
            try:
                res.set_property_value(name, propvalue, dry_run=True)
            except Exception as e:
                writeresult = as_DAVError(e)
            else:
                writeresult = "200 OK"
            writeresultlist.append((name, writeresult))
            successflag = successflag and writeresult == "200 OK"

        # Generate response list of 2-tuples (name, value)
        # <value> is None on success, or an instance of DAVError
        propResponseList = []
        responsedescription = []

        if not successflag:
            # If dry run failed: convert all OK to FAILED_DEPENDENCY.
            for (name, result) in writeresultlist:
                if result == "200 OK":
                    result = DAVError(HTTP_FAILED_DEPENDENCY)
                elif isinstance(result, DAVError):
                    responsedescription.append(result.get_user_info())
                propResponseList.append((name, result))

        else:
            # Dry-run succeeded: set properties again, this time in 'real' mode
            # In theory, there should be no exceptions thrown here, but this is
            # real live...
            for (name, propvalue) in propupdatelist:
                try:
                    res.set_property_value(name, propvalue, dry_run=False)
                    # Set value to None, so the response xml contains empty tags
                    propResponseList.append((name, None))
                except Exception as e:
                    e = as_DAVError(e)
                    propResponseList.append((name, e))
                    responsedescription.append(e.get_user_info())

        # Generate response XML
        multistatusEL = xml_tools.make_multistatus_el()
        href = res.get_href()
        util.add_property_response(multistatusEL, href, propResponseList)
        if responsedescription:
            etree.SubElement(
                multistatusEL, "{DAV:}responsedescription"
            ).text = "\n".join(responsedescription)

        # Send response
        return util.send_multi_status_response(environ, start_response, multistatusEL)