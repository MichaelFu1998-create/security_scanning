def sha_github_file(cls, config, repo_file, repository_api, repository_branch):
        """ Return the GitHub SHA for a file in the repository """

        repo_file_sha = None

        cfg = config.get_conf()
        github_token = cfg['sortinghat']['identities_api_token']
        headers = {"Authorization": "token " + github_token}

        url_dir = repository_api + "/git/trees/" + repository_branch
        logger.debug("Gettting sha data from tree: %s", url_dir)
        raw_repo_file_info = requests.get(url_dir, headers=headers)
        raw_repo_file_info.raise_for_status()
        for rfile in raw_repo_file_info.json()['tree']:
            if rfile['path'] == repo_file:
                logger.debug("SHA found: %s, ", rfile["sha"])
                repo_file_sha = rfile["sha"]
                break

        return repo_file_sha