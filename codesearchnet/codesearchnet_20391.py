def requirements_for_changes(self, changes):
        """
        Parse changes for requirements

        :param list changes:
        """
        requirements = []
        reqs_set = set()

        if isinstance(changes, str):
            changes = changes.split('\n')

        if not changes or changes[0].startswith('-'):
            return requirements

        for line in changes:
            line = line.strip(' -+*')

            if not line:
                continue

            match = IS_REQUIREMENTS_RE2.search(line)  # or  IS_REQUIREMENTS_RE.match(line)
            if match:
                for match in REQUIREMENTS_RE.findall(match.group(1)):
                    if match[1]:
                        version = '==' + match[2] if match[1].startswith(' to ') else match[1]
                        req_str = match[0] + version
                    else:
                        req_str = match[0]

                    if req_str not in reqs_set:
                        reqs_set.add(req_str)
                        try:
                            requirements.append(pkg_resources.Requirement.parse(req_str))
                        except Exception as e:
                            log.warn('Could not parse requirement "%s" from changes: %s', req_str, e)

        return requirements