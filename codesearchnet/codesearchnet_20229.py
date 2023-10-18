def post(repo, args=[]):
    """
    Post to metadata server

    Parameters
    ----------

    repo: Repository object (result of lookup)
    """

    mgr = plugins_get_mgr()
    keys = mgr.search(what='metadata')
    keys = keys['metadata']

    if len(keys) == 0:
        return

    # Incorporate pipeline information...
    if 'pipeline' in repo.options:
        for name, details in repo.options['pipeline'].items():
            patterns = details['files']
            matching_files = repo.find_matching_files(patterns)
            matching_files.sort()
            details['files'] = matching_files
            for i, f in enumerate(matching_files):
                r = repo.get_resource(f)
                if 'pipeline' not in r:
                    r['pipeline'] = []
                r['pipeline'].append(name + " [Step {}]".format(i))

    if 'metadata-management' in repo.options:

        print("Collecting all the required metadata to post")
        metadata = repo.options['metadata-management']

        # Add data repo history
        if 'include-data-history' in metadata and metadata['include-data-history']:
            repo.package['history'] = get_history(repo.rootdir)

        # Add action history 
        if 'include-action-history' in metadata and metadata['include-action-history']:
            annotate_metadata_action(repo) 

        # Add data repo history
        if 'include-preview' in metadata:
            annotate_metadata_data(repo,
                                   task='preview',
                                   patterns=metadata['include-preview']['files'],
                                   size=metadata['include-preview']['length'])

        if (('include-schema' in metadata) and metadata['include-schema']):
            annotate_metadata_data(repo,  task='schema')

        if 'include-code-history' in metadata:
            annotate_metadata_code(repo, files=metadata['include-code-history'])

        if 'include-platform' in metadata:
            annotate_metadata_platform(repo)

        if 'include-validation' in metadata:
            annotate_metadata_validation(repo)

        if 'include-dependencies' in metadata:
            annotate_metadata_dependencies(repo)

        history = repo.package.get('history',None)
        if (('include-tab-diffs' in metadata) and
            metadata['include-tab-diffs'] and
            history is not None):
            annotate_metadata_diffs(repo)

        # Insert options as well
        repo.package['config'] = repo.options

    try:
        for k in keys:
            # print("Key", k)
            metadatamgr = mgr.get_by_key('metadata', k)
            url = metadatamgr.url
            o = urlparse(url)
            print("Posting to ", o.netloc)
            response = metadatamgr.post(repo)
            if isinstance(response, str):
                print("Error while posting:", response)
            elif response.status_code in [400]:
                content = response.json()
                print("Error while posting:")
                for k in content:
                    print("   ", k,"- ", ",".join(content[k]))
    except NetworkError as e:
        print("Unable to reach metadata server!")
    except NetworkInvalidConfiguration as e:
        print("Invalid network configuration in the INI file")
        print(e.message)
    except Exception as e:
        print("Could not post. Unknown error")
        print(e)