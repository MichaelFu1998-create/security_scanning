def add(self, requirements, required=None):
        """
        Add requirements to be managed

        :param list/Requirement requirements: List of :class:`BumpRequirement` or :class:`pkg_resources.Requirement`
        :param bool required: Set required flag for each requirement if provided.
        """
        if isinstance(requirements, RequirementsManager):
            requirements = list(requirements)
        elif not isinstance(requirements, list):
            requirements = [requirements]

        for req in requirements:
            name = req.project_name

            if not isinstance(req, BumpRequirement):
                req = BumpRequirement(req, required=required)
            elif required is not None:
                req.required = required

            add = True

            if name in self.requirements:
                for existing_req in self.requirements[name]:
                    if req == existing_req:
                        add = False
                        break

                    # Need to replace existing as the new req will be used to bump next, and req.required could be
                    # updated.
                    replace = False

                    # Two pins: Use highest pinned version
                    if (req.specs and req.specs[0][0] == '==' and existing_req.specs and
                            existing_req.specs[0][0] == '=='):
                        if pkg_resources.parse_version(req.specs[0][1]) < pkg_resources.parse_version(
                                existing_req.specs[0][1]):
                            req.requirement = existing_req.requirement
                        replace = True

                    # Replace Any
                    if not (req.specs and existing_req.specs):
                        if existing_req.specs:
                            req.requirement = existing_req.requirement
                        replace = True

                    if replace:
                        req.required |= existing_req.required
                        if existing_req.required_by and not req.required_by:
                            req.required_by = existing_req.required_by
                        self.requirements[name].remove(existing_req)
                        break

            if add:
                self.requirements[name].append(req)