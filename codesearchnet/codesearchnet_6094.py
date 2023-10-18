def get_property_names(self, is_allprop):
        """Return list of supported property names in Clark Notation.

        Note that 'allprop', despite its name, which remains for
        backward-compatibility, does not return every property, but only dead
        properties and the live properties defined in RFC4918.

        This default implementation returns a combination of:

        - Supported standard live properties in the {DAV:} namespace, if the
          related getter method returns not None.
        - {DAV:}lockdiscovery and {DAV:}supportedlock, if a lock manager is
          present
        - If a property manager is present, then a list of dead properties is
          appended

        A resource provider may override this method, to add a list of
        supported custom live property names.
        """
        # Live properties
        propNameList = []

        propNameList.append("{DAV:}resourcetype")

        if self.get_creation_date() is not None:
            propNameList.append("{DAV:}creationdate")
        if self.get_content_length() is not None:
            assert not self.is_collection
            propNameList.append("{DAV:}getcontentlength")
        if self.get_content_type() is not None:
            propNameList.append("{DAV:}getcontenttype")
        if self.get_last_modified() is not None:
            propNameList.append("{DAV:}getlastmodified")
        if self.get_display_name() is not None:
            propNameList.append("{DAV:}displayname")
        if self.get_etag() is not None:
            propNameList.append("{DAV:}getetag")

        # Locking properties
        if self.provider.lock_manager and not self.prevent_locking():
            propNameList.extend(_lockPropertyNames)

        # Dead properties
        if self.provider.prop_manager:
            refUrl = self.get_ref_url()
            propNameList.extend(
                self.provider.prop_manager.get_properties(refUrl, self.environ)
            )

        return propNameList