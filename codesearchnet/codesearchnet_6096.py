def get_property_value(self, name):
        """Return the value of a property.

        name:
            the property name in Clark notation.
        return value:
            may have different types, depending on the status:

            - string or unicode: for standard property values.
            - lxml.etree.Element: for complex values.

            If the property is not available, a DAVError is raised.

        This default implementation handles ``{DAV:}lockdiscovery`` and
        ``{DAV:}supportedlock`` using the associated lock manager.

        All other *live* properties (i.e. name starts with ``{DAV:}``) are
        delegated to the self.xxx() getters.

        Finally, other properties are considered *dead*, and are handled  by
        the associated property manager.
        """
        refUrl = self.get_ref_url()

        # lock properties
        lm = self.provider.lock_manager
        if lm and name == "{DAV:}lockdiscovery":
            # TODO: we return HTTP_NOT_FOUND if no lockmanager is present.
            # Correct?
            activelocklist = lm.get_url_lock_list(refUrl)
            lockdiscoveryEL = etree.Element(name)
            for lock in activelocklist:
                activelockEL = etree.SubElement(lockdiscoveryEL, "{DAV:}activelock")

                locktypeEL = etree.SubElement(activelockEL, "{DAV:}locktype")
                # Note: make sure `{DAV:}` is not handled as format tag:
                etree.SubElement(locktypeEL, "{}{}".format("{DAV:}", lock["type"]))

                lockscopeEL = etree.SubElement(activelockEL, "{DAV:}lockscope")
                # Note: make sure `{DAV:}` is not handled as format tag:
                etree.SubElement(lockscopeEL, "{}{}".format("{DAV:}", lock["scope"]))

                etree.SubElement(activelockEL, "{DAV:}depth").text = lock["depth"]
                if lock["owner"]:
                    # lock["owner"] is an XML string
                    # owner may be empty (#64)
                    ownerEL = xml_tools.string_to_xml(lock["owner"])
                    activelockEL.append(ownerEL)

                timeout = lock["timeout"]
                if timeout < 0:
                    timeout = "Infinite"
                else:
                    # The time remaining on the lock
                    expire = lock["expire"]
                    timeout = "Second-" + str(int(expire - time.time()))
                etree.SubElement(activelockEL, "{DAV:}timeout").text = timeout

                locktokenEL = etree.SubElement(activelockEL, "{DAV:}locktoken")
                etree.SubElement(locktokenEL, "{DAV:}href").text = lock["token"]

                # TODO: this is ugly:
                #       res.get_property_value("{DAV:}lockdiscovery")
                #
                #                lockRoot = self.get_href(self.provider.ref_url_to_path(lock["root"]))
                lockPath = self.provider.ref_url_to_path(lock["root"])
                lockRes = self.provider.get_resource_inst(lockPath, self.environ)
                # FIXME: test for None
                lockHref = lockRes.get_href()

                lockrootEL = etree.SubElement(activelockEL, "{DAV:}lockroot")
                etree.SubElement(lockrootEL, "{DAV:}href").text = lockHref

            return lockdiscoveryEL

        elif lm and name == "{DAV:}supportedlock":
            # TODO: we return HTTP_NOT_FOUND if no lockmanager is present. Correct?
            # TODO: the lockmanager should decide about it's features
            supportedlockEL = etree.Element(name)

            lockentryEL = etree.SubElement(supportedlockEL, "{DAV:}lockentry")
            lockscopeEL = etree.SubElement(lockentryEL, "{DAV:}lockscope")
            etree.SubElement(lockscopeEL, "{DAV:}exclusive")
            locktypeEL = etree.SubElement(lockentryEL, "{DAV:}locktype")
            etree.SubElement(locktypeEL, "{DAV:}write")

            lockentryEL = etree.SubElement(supportedlockEL, "{DAV:}lockentry")
            lockscopeEL = etree.SubElement(lockentryEL, "{DAV:}lockscope")
            etree.SubElement(lockscopeEL, "{DAV:}shared")
            locktypeEL = etree.SubElement(lockentryEL, "{DAV:}locktype")
            etree.SubElement(locktypeEL, "{DAV:}write")

            return supportedlockEL

        elif name.startswith("{DAV:}"):
            # Standard live property (raises HTTP_NOT_FOUND if not supported)
            if name == "{DAV:}creationdate" and self.get_creation_date() is not None:
                # Note: uses RFC3339 format (ISO 8601)
                return util.get_rfc3339_time(self.get_creation_date())
            elif name == "{DAV:}getcontenttype" and self.get_content_type() is not None:
                return self.get_content_type()
            elif name == "{DAV:}resourcetype":
                if self.is_collection:
                    resourcetypeEL = etree.Element(name)
                    etree.SubElement(resourcetypeEL, "{DAV:}collection")
                    return resourcetypeEL
                return ""
            elif (
                name == "{DAV:}getlastmodified" and self.get_last_modified() is not None
            ):
                # Note: uses RFC1123 format
                return util.get_rfc1123_time(self.get_last_modified())
            elif (
                name == "{DAV:}getcontentlength"
                and self.get_content_length() is not None
            ):
                # Note: must be a numeric string
                return str(self.get_content_length())
            elif name == "{DAV:}getetag" and self.get_etag() is not None:
                return self.get_etag()
            elif name == "{DAV:}displayname" and self.get_display_name() is not None:
                return self.get_display_name()

            # Unsupported, no persistence available, or property not found
            raise DAVError(HTTP_NOT_FOUND)

        # Dead property
        pm = self.provider.prop_manager
        if pm:
            value = pm.get_property(refUrl, name, self.environ)
            if value is not None:
                return xml_tools.string_to_xml(value)

        # No persistence available, or property not found
        raise DAVError(HTTP_NOT_FOUND)