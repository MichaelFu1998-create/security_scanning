def build_org(self, doc, entity):
        """Builds an organization object of of a string representation.
        Returns built organization. Raises SPDXValueError if failed to extract
        name.
        """
        match = self.org_re.match(entity)
        if match and validations.validate_org_name(match.group(self.ORG_NAME_GROUP)):
            name = match.group(self.ORG_NAME_GROUP).strip()
            email = match.group(self.ORG_EMAIL_GROUP)
            if (email is not None) and (len(email) != 0):
                return creationinfo.Organization(name=name, email=email.strip())
            else:
                return creationinfo.Organization(name=name, email=None)
        else:
            raise SPDXValueError('Failed to extract Organization name')