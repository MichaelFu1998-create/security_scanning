def bump(self, filter_requirements, required=False, show_summary=True, show_detail=False, **kwargs):
        """
        Bump dependency requirements using filter.

        :param list filter_requirements: List of dependency filter requirements.
        :param bool required: Require the filter_requirements to be met (by adding if possible).
        :param bool show_summary: Show summary for each bump made.
        :param bool show_detail: Show detail for each bump made if available.
        :return: Tuple with two elements: Dict of target file to bump message, List of :class:`Bump`
        :raise BumpAccident: for any bump errors
        """
        found_targets = [target for target in self.targets if os.path.exists(target)]

        if not found_targets:
            raise BumpAccident('None of the requirement file(s) were found: %s' % ', '.join(self.targets))

        bump_reqs = RequirementsManager()

        if filter_requirements:
            requirements = parse_requirements(filter_requirements)
            bump_reqs.add(requirements, required=required)

        try:

            for target in found_targets:
                log.debug('Target: %s', target)

                target_bumpers = []
                target_bump_reqs = RequirementsManager(bump_reqs)
                loops = 0

                while True:

                    # Insurance to ensure that we don't get stuck forever.
                    loops += 1
                    if loops > 5:
                        log.debug('Too many transitive bump loops. Bailing out.')
                        break

                    if not target_bumpers:
                        target_bumpers = [model(target, detail=self.detail, test_drive=self.test_drive)
                                          for model in self.bumper_models if model.likes(target)]

                        if not target_bumpers:
                            log.debug('No bumpers found that can bump %s. Defaulting to %s', target, self.default_model)
                            target_bumpers = [self.default_model(target, detail=self.detail,
                                                                 test_drive=self.test_drive)]

                        self.bumpers.extend(target_bumpers)

                    new_target_bump_reqs = RequirementsManager()

                    for bumper in target_bumpers:
                        target_bumps = bumper.bump(target_bump_reqs)
                        self.bumps.update(dict((b.name, b) for b in target_bumps))

                        for bump in target_bumps:
                            for new_req in bump.requirements:
                                if not (bump_reqs.satisfied_by_checked(new_req) or
                                        target_bump_reqs.satisfied_by_checked(new_req)):
                                    new_target_bump_reqs.add(new_req)

                    bump_reqs.matched_name |= target_bump_reqs.matched_name
                    bump_reqs.checked.extend(target_bump_reqs.checked)

                    if new_target_bump_reqs:
                        bump_reqs.add(new_target_bump_reqs)

                    target_bump_reqs = RequirementsManager(list(
                        r for r in new_target_bump_reqs if r.project_name not in self.bumps))

                    if not target_bump_reqs:
                        break

            if not self.bumpers:
                raise BumpAccident('No bumpers found for %s' % ', '.join(found_targets))

            if bump_reqs and not bump_reqs.matched_name:
                raise BumpAccident('None of the provided filter names were found in %s' % ', '.join(found_targets))

            if self.bumps:
                for bump in self.bumps.values():
                    bump_reqs.check(bump)

                for reqs in bump_reqs.required_requirements().values():
                    for req in reqs:
                        if not self.full_throttle:
                            use_force = 'Use --force to ignore / force the bump' if req.required_by else ''
                            raise BumpAccident('Requirement "%s" could not be met so '
                                               'bump can not proceed. %s' % (req, use_force))

                if self.test_drive:
                    log.info("Changes that would be made:\n")

                messages = {}

                for bumper in self.bumpers:
                    if bumper.bumps:
                        if not self.test_drive:
                            bumper.update_requirements()

                        if self.test_drive or show_summary:
                            msg = bumper.bump_message(self.test_drive or show_detail)

                            if self.test_drive:
                                print(msg)
                            else:
                                rewords = [('Bump ', 'Bumped '), ('Pin ', 'Pinned '),
                                           ('Require ', 'Updated requirements: ')]
                                for word, new_word in rewords:
                                    if msg.startswith(word):
                                        msg = msg.replace(word, new_word, 1)
                                        break
                                log.info(msg)

                        messages[bumper.target] = bumper.bump_message(True)

                return messages, self.bumps

            else:
                log.info('No need to bump. Everything is up to date!')
                return {}, []

        except Exception:
            if not self.test_drive and self.bumps:
                map(lambda b: b.reverse(), self.bumpers)
            raise