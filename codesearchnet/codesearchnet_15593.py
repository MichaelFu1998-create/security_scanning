def user_project_from_option(options, arg0, arg1):
        """
        Try to find user and project name from git remote output

        @param [String] output of git remote command
        @return [Array] user and project
        """

        site = options.github_site
        if arg0 and not arg1:
            # this match should parse strings such as
            #   "https://github.com/skywinder/Github-Changelog-Generator"
            # or
            #   "skywinder/Github-Changelog-Generator"
            #  to user and project
            match = re.match(
                "(?:.+{site}/)?(.+)/(.+)".format(site=site),
                arg0
            )
            if not match:
                print("Can't detect user and name from first "
                      "parameter: '{arg0}' -> exit'".format(arg0=arg0))
                exit(1)
            return match.groups()
        return None, None