def as_requirement(self):
        """ Convert back to a :class:`pkg_resources.Requirement` instance """
        if self.new_version:
            return pkg_resources.Requirement.parse(self.name + ''.join(self.new_version))
        else:
            return pkg_resources.Requirement.parse(self.name)