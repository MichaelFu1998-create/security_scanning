def check(self, context, version=None):
        """
        Check off requirements that are met by name/version.

        :param str|Bump|Requirement context: Either package name, requirement string, :class:`Bump`,
                                             :class:`BumpRequirement`, or
                                             :class:`pkg_resources.Requirement instance
        :return: True if any requirement was satisified by context
        """
        req_str = None

        self.checked.append((context, version))

        if isinstance(context, str) and not version:
            context = BumpRequirement.parse(context)

        if isinstance(context, Bump):
            name = context.name
            if context.new_version and context.new_version[0] == '==':
                version = context.new_version[1]
            else:
                req_str = str(context)

        elif isinstance(context, (pkg_resources.Requirement, BumpRequirement)):
            name = context.project_name
            if context.specs and context.specs[0][0] == '==':
                version = context.specs[0][1]
            else:
                req_str = str(context)

        else:
            name = context

        if name in self:
            self.matched_name = True

            for req in self[name]:
                if req.required and (version and version in req or req_str == str(req)):
                    req.required = False
                    return True

        return False