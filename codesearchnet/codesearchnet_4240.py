def build_person(self, doc, entity):
        """Builds an organization object of of a string representation.
        Returns built organization. Raises SPDXValueError if failed to extract
        name.
        """
        match = self.person_re.match(entity)
        if match and validations.validate_person_name(match.group(self.PERSON_NAME_GROUP)):
            name = match.group(self.PERSON_NAME_GROUP).strip()
            email = match.group(self.PERSON_EMAIL_GROUP)
            if (email is not None) and (len(email) != 0):
                return creationinfo.Person(name=name, email=email.strip())
            else:
                return creationinfo.Person(name=name, email=None)
        else:
            raise SPDXValueError('Failed to extract person name')