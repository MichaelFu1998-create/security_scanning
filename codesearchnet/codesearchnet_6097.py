def set_property_value(self, name, value, dry_run=False):
        """Set a property value or remove a property.

        value == None means 'remove property'.
        Raise HTTP_FORBIDDEN if property is read-only, or not supported.

        When dry_run is True, this function should raise errors, as in a real
        run, but MUST NOT change any data.

        This default implementation

        - raises HTTP_FORBIDDEN, if trying to modify a locking property
        - raises HTTP_FORBIDDEN, if trying to modify an immutable {DAV:}
          property
        - handles Windows' Win32LastModifiedTime to set the getlastmodified
          property, if enabled
        - stores everything else as dead property, if a property manager is
          present.
        - raises HTTP_FORBIDDEN, else

        Removing a non-existing prop is NOT an error.

        Note: RFC 4918 states that {DAV:}displayname 'SHOULD NOT be protected'

        A resource provider may override this method, to update supported custom
        live properties.
        """
        assert value is None or xml_tools.is_etree_element(value)

        if name in _lockPropertyNames:
            # Locking properties are always read-only
            raise DAVError(
                HTTP_FORBIDDEN, err_condition=PRECONDITION_CODE_ProtectedProperty
            )

        # Live property
        config = self.environ["wsgidav.config"]
        # hotfixes = config.get("hotfixes", {})
        mutableLiveProps = config.get("mutable_live_props", [])
        # Accept custom live property updates on resources if configured.
        if (
            name.startswith("{DAV:}")
            and name in _standardLivePropNames
            and name in mutableLiveProps
        ):
            # Please note that some properties should not be mutable according
            # to RFC4918. This includes the 'getlastmodified' property, which
            # it may still make sense to make mutable in order to support time
            # stamp changes from e.g. utime calls or the touch or rsync -a
            # commands.
            if name in ("{DAV:}getlastmodified", "{DAV:}last_modified"):
                try:
                    return self.set_last_modified(self.path, value.text, dry_run)
                except Exception:
                    _logger.warning(
                        "Provider does not support set_last_modified on {}.".format(
                            self.path
                        )
                    )

            # Unsupported or not allowed
            raise DAVError(HTTP_FORBIDDEN)

        # Handle MS Windows Win32LastModifiedTime, if enabled.
        # Note that the WebDAV client in Win7 and earler has issues and can't be used
        # with this so we ignore older clients. Others pre-Win10 should be tested.
        if name.startswith("{urn:schemas-microsoft-com:}"):
            agent = self.environ.get("HTTP_USER_AGENT", "None")
            win32_emu = config.get("hotfixes", {}).get("emulate_win32_lastmod", False)
            if win32_emu and "MiniRedir/6.1" not in agent:
                if "Win32LastModifiedTime" in name:
                    return self.set_last_modified(self.path, value.text, dry_run)
                elif "Win32FileAttributes" in name:
                    return True
                elif "Win32CreationTime" in name:
                    return True
                elif "Win32LastAccessTime" in name:
                    return True

        # Dead property
        pm = self.provider.prop_manager
        if pm and not name.startswith("{DAV:}"):
            refUrl = self.get_ref_url()
            if value is None:
                return pm.remove_property(refUrl, name, dry_run, self.environ)
            else:
                value = etree.tostring(value)
                return pm.write_property(refUrl, name, value, dry_run, self.environ)

        raise DAVError(HTTP_FORBIDDEN)