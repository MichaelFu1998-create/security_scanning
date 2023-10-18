def from_requirement(cls, req, changes=None):
        """ Create an instance from :class:`pkg_resources.Requirement` instance """
        return cls(req.project_name, req.specs and ''.join(req.specs[0]) or '', changes=changes)