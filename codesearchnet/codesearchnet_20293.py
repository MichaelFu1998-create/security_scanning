def get_tree(gitdir="."):
    """
    Get the commit history for a given dataset
    """

    cmd = ["git", "log", "--all", "--branches", '--pretty=format:{  "commit": "%H",  "abbreviated_commit": "%h",  "tree": "%T",  "abbreviated_tree": "%t",  "parent": "%P",  "abbreviated_parent": "%p",  "refs": "%d",  "encoding": "%e",  "subject": "%s", "sanitized_subject_line": "%f",  "commit_notes": "",  "author": {    "name": "%aN",    "email": "%aE",    "date": "%ai"  },  "commiter": {    "name": "%cN",    "email": "%cE",    "date": "%ci"  }},']

    output = run(cmd)
    lines = output.split("\n")

    content = ""
    history = []
    for l in lines:
        try:
            revisedcontent = content + l
            if revisedcontent.count('"') % 2 == 0:
                j = json.loads(revisedcontent[:-1])
                if "Notes added by" in j['subject']:
                    content = ""
                    continue
                history.append(j)
                content = ""
            else:
                content = revisedcontent
        except Exception as e:
            print("Error while parsing record")
            print(revisedcontent)
            content = ""

    # Order by time. First commit first...
    history.reverse()

    #
    changes = get_change()

    for i in range(len(history)):
        abbrev_commit = history[i]['abbreviated_commit']
        if abbrev_commit not in changes:
            raise Exception("Missing changes for " + abbrev_commit)

        history[i]['changes'] = changes[abbrev_commit]['changes']


    return history