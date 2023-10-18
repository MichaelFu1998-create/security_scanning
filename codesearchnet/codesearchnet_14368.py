def ls(github_user, template, long_format):
    """
    List packages created with temple. Enter a github user or
    organization to list all templates under the user or org.
    Using a template path as the second argument will list all projects
    that have been started with that template.

    Use "-l" to print the Github repository descriptions of templates
    or projects.
    """
    github_urls = temple.ls.ls(github_user, template=template)
    for ssh_path, info in github_urls.items():
        if long_format:
            print(ssh_path, '-', info['description'] or '(no project description found)')
        else:
            print(ssh_path)