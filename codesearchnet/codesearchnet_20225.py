def annotate_metadata_code(repo, files):
    """
    Update metadata with the commit information
    """

    package = repo.package
    package['code'] = []
    for p in files:
        matching_files = glob2.glob("**/{}".format(p))
        for f in matching_files:
            absf = os.path.abspath(f)
            print("Add commit data for {}".format(f))
            package['code'].append(OrderedDict([
                ('script', f),
                ('permalink', repo.manager.permalink(repo, absf)),
                ('mimetypes', mimetypes.guess_type(absf)[0]),
                ('sha256', compute_sha256(absf))
            ]))