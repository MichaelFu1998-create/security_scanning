def _bump(self, existing_req=None, bump_reqs=None):
        """
          Bump an existing requirement to the desired requirement if any.
          Subclass can override this `_bump` method to change how each requirement is bumped.

          BR = Bump to Requested Version
          BL = Bump to Latest Version
          BLR = Bump to Latest Version per Requested Requirement
          BROL = Bump to Requested Version or Latest (if Pin)
          N = No Bump
          ERR = Error
          C = Version Conflict

          Pin case "requires=" will be required.
          Filter case "requires=" will be:
             1) From user = Required
             2) From bump = bump/require if existing = One, otherwise print warning.

          Filter Case::
              Bump:    None  Any  One  Many
          Existing:
               None    N     N    N    N
                Any    N     N    BR   BR
                One    BL    BL   BR   BR
               Many    N     N    BR   BR

          Pin Case::
              Bump:    None  Any  One  Many
          Existing:
               None    N     N    N    N
                Any    N     N    BR   BLR*
                One    BL    BL   BR   BLR*
               Many    N     N    BR   BLR*

          Add/Require Case::
              Bump:    None  Any  One  Many
          Existing:
               None    N     BROL BROL BROL

          :param pkg_resources.Requirement existing_req: Existing requirement if any
          :param list bump_reqs: List of `BumpRequirement`
          :return Bump: Either a :class:`Bump` instance or None
          :raise BumpAccident:
        """
        if existing_req or bump_reqs and any(r.required for r in bump_reqs):
            name = existing_req and existing_req.project_name or bump_reqs[0].project_name

            log.info('Checking %s', name)

            bump = current_version = new_version = None

            if bump_reqs:
                # BLR: Pin with Many bump requirements
                if self.should_pin() and (len(bump_reqs) > 1 or bump_reqs[0] and
                                          bump_reqs[0].specs and bump_reqs[0].specs[0][0] != '=='):
                    log.debug('Bump to latest within requirements: %s', bump_reqs)

                    new_version = self.latest_version_for_requirements(bump_reqs)
                    current_version = (existing_req and existing_req.specs and existing_req.specs[0][0] == '==' and
                                       existing_req.specs[0][1])

                    if current_version == new_version:
                        return None

                    bump = Bump(name, ('==', new_version))

                elif len(bump_reqs) > 1:
                    raise BumpAccident('Not sure which requirement to use for %s: %s' % (
                        name, ', '.join(str(r) for r in bump_reqs)))

                # BR: Pin with One bump requirement or Filter with One or Many bump requirements or
                #     Bump to Any required.
                elif bump_reqs[0].specs or not (existing_req or self.should_pin() or bump_reqs[0].specs):
                    log.debug('Bump to requirement: %s', bump_reqs)

                    latest_version = self.latest_version_for_requirements(bump_reqs)

                    new_version = (bump_reqs[0].specs and bump_reqs[0].specs[0][0] == '==' and
                                   bump_reqs[0].specs[0][1] or latest_version)
                    current_version = (existing_req and existing_req.specs and existing_req.specs[0][0] == '==' and
                                       existing_req.specs[0][1])

                    if current_version == new_version:
                        return None

                    if len(bump_reqs[0].specs) > 1:
                        version = (','.join(s[0] + s[1] for s in bump_reqs[0].specs),)
                    elif bump_reqs[0].specs:
                        version = bump_reqs[0].specs[0]
                    else:
                        version = None
                    bump = Bump(name, version)

            # BL: Pin to Latest
            if not bump and (existing_req and existing_req.specs and existing_req.specs[0][0] == '==' or
                             self.should_pin() and not existing_req):
                log.debug('Bump to latest: %s', bump_reqs or name)

                current_version = existing_req and existing_req.specs[0][1]
                new_version = self.latest_package_version(name)

                if current_version == new_version:
                    return None

                if not new_version:
                    raise BumpAccident('No published version found for %s' % name)

                bump = Bump(name, ('==', new_version))

            if bump and current_version and new_version and self.detail:
                changes = self.package_changes(bump.name, current_version, new_version)
                bump.changes.extend(changes)
                if self.should_pin():
                    bump.require(self.requirements_for_changes(changes))

            if bump:
                log.debug('Bumped %s', bump)

                if bump.requirements:
                    log.info('Changes in %s require: %s',
                             bump.name, ', '.join(sorted(str(r) for r in bump.requirements)))

            return bump if str(bump) != str(existing_req) else None