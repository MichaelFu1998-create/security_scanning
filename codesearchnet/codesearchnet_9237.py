def get_repos_by_backend_section(cls, backend_section, raw=True):
        """ return list with the repositories for a backend_section """
        repos = []
        projects = TaskProjects.get_projects()

        for pro in projects:
            if backend_section in projects[pro]:
                # if the projects.json doesn't contain the `unknown` project, add the repos in the bck section
                if cls.GLOBAL_PROJECT not in projects:
                    repos += projects[pro][backend_section]
                else:
                    # if the projects.json contains the `unknown` project
                    # in the case of the collection phase
                    if raw:
                        # if the current project is not `unknown`
                        if pro != cls.GLOBAL_PROJECT:
                            # if the bck section is not in the `unknown` project, add the repos in the bck section
                            if backend_section not in projects[cls.GLOBAL_PROJECT]:
                                repos += projects[pro][backend_section]
                            # if the backend section is in the `unknown` project,
                            # add the repo in the bck section under `unknown`
                            elif backend_section in projects[pro] and backend_section in projects[cls.GLOBAL_PROJECT]:
                                repos += projects[cls.GLOBAL_PROJECT][backend_section]
                        # if the current project is `unknown`
                        else:
                            # if the backend section is only in the `unknown` project,
                            # add the repo in the bck section under `unknown`
                            not_in_unknown = [projects[pro] for pro in projects if pro != cls.GLOBAL_PROJECT][0]
                            if backend_section not in not_in_unknown:
                                repos += projects[cls.GLOBAL_PROJECT][backend_section]
                    # in the case of the enrichment phase
                    else:
                        # if the current project is not `unknown`
                        if pro != cls.GLOBAL_PROJECT:
                            # if the bck section is not in the `unknown` project, add the repos in the bck section
                            if backend_section not in projects[cls.GLOBAL_PROJECT]:
                                repos += projects[pro][backend_section]
                            # if the backend section is in the `unknown` project, add the repos in the bck section
                            elif backend_section in projects[pro] and backend_section in projects[cls.GLOBAL_PROJECT]:
                                repos += projects[pro][backend_section]
                        # if the current project is `unknown`
                        else:
                            # if the backend section is only in the `unknown` project,
                            # add the repo in the bck section under `unknown`
                            not_in_unknown_prj = [projects[prj] for prj in projects if prj != cls.GLOBAL_PROJECT]
                            not_in_unknown_sections = list(set([section for prj in not_in_unknown_prj
                                                                for section in list(prj.keys())]))
                            if backend_section not in not_in_unknown_sections:
                                repos += projects[pro][backend_section]

        logger.debug("List of repos for %s: %s (raw=%s)", backend_section, repos, raw)

        # avoid duplicated repos
        repos = list(set(repos))

        return repos