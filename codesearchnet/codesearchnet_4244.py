def set_lics_list_ver(self, doc, value):
        """Sets the license list version, Raises CardinalityError if
        already set, SPDXValueError if incorrect value.
        """
        if not self.lics_list_ver_set:
            self.lics_list_ver_set = True
            vers = version.Version.from_str(value)
            if vers is not None:
                doc.creation_info.license_list_version = vers
                return True
            else:
                raise SPDXValueError('CreationInfo::LicenseListVersion')
        else:
            raise CardinalityError('CreationInfo::LicenseListVersion')