def require(self, req):
        """ Add new requirements that must be fulfilled for this bump to occur """
        reqs = req if isinstance(req, list) else [req]

        for req in reqs:
            if not isinstance(req, BumpRequirement):
                req = BumpRequirement(req)
            req.required = True
            req.required_by = self
            self.requirements.append(req)