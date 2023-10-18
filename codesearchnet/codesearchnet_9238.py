def convert_from_eclipse(self, eclipse_projects):
        """ Convert from eclipse projects format to grimoire projects json format """

        projects = {}

        # We need the global project for downloading the full Bugzilla and Gerrit
        projects['unknown'] = {
            "gerrit": ["git.eclipse.org"],
            "bugzilla": ["https://bugs.eclipse.org/bugs/"]
        }

        projects = compose_title(projects, eclipse_projects)
        projects = compose_projects_json(projects, eclipse_projects)

        return projects