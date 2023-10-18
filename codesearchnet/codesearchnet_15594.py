def user_project_from_remote(remote):
        """
        Try to find user and project name from git remote output

        @param [String] output of git remote command
        @return [Array] user and project
        """

        # try to find repo in format:
        # origin	git@github.com:skywinder/Github-Changelog-Generator.git (fetch)
        # git@github.com:skywinder/Github-Changelog-Generator.git
        regex1 = br".*(?:[:/])(?P<user>(-|\w|\.)*)/" \
                 br"(?P<project>(-|\w|\.)*)(\.git).*"
        match = re.match(regex1, remote)
        if match:
            return match.group("user"), match.group("project")

        # try to find repo in format:
        # origin	https://github.com/skywinder/ChangelogMerger (fetch)
        # https://github.com/skywinder/ChangelogMerger
        regex2 = r".*/((?:-|\w|\.)*)/((?:-|\w|\.)*).*"
        match = re.match(regex2, remote)
        if match:
            return match.group("user"), match.group("project")

        return None, None