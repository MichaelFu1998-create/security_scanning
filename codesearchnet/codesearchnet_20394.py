def bump(self, bump_reqs=None, **kwargs):
        """
          Bump dependencies using given requirements.

          :param RequirementsManager bump_reqs: Bump requirements manager
          :param dict kwargs: Additional args from argparse. Some bumpers accept user options, and some not.
          :return: List of :class:`Bump` changes made.
        """

        bumps = {}

        for existing_req in sorted(self.requirements(), key=lambda r: r.project_name):
            if bump_reqs and existing_req.project_name not in bump_reqs:
                continue

            bump_reqs.check(existing_req)

            try:
                bump = self._bump(existing_req, bump_reqs.get(existing_req.project_name))

                if bump:
                    bumps[bump.name] = bump
                    bump_reqs.check(bump)

            except Exception as e:
                if bump_reqs and bump_reqs.get(existing_req.project_name) and all(
                        r.required_by is None for r in bump_reqs.get(existing_req.project_name)):
                    raise
                else:
                    log.warn(e)

        for reqs in bump_reqs.required_requirements().values():
            name = reqs[0].project_name
            if name not in bumps and self.should_add(name):
                try:
                    bump = self._bump(None, reqs)

                    if bump:
                        bumps[bump.name] = bump
                        bump_reqs.check(bump)

                except Exception as e:
                    if all(r.required_by is None for r in reqs):
                        raise
                    else:
                        log.warn(e)

        self.bumps.update(bumps.values())

        return bumps.values()