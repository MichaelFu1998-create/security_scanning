def delete(repo, args=[]):
    """
    Delete files

    Parameters
    ----------

    repo: Repository object
    args: Arguments to git command
    """

    # Remove the files 
    result = generic_repo_cmd(repo, 'delete', args)
    if result['status'] != 'success': 
        return status 

    with cd(repo.rootdir): 
        
        package = repo.package 
        resources = package['resources'] 

        cleaned_resources = []
        for r in resources: 
            relativepath = r['relativepath'] 
            sha256 = r['sha256'] 
            if relativepath not in ['', None]: 
                if not os.path.exists(relativepath): 
                    # This file does not exist on disk. 
                    print("Skipping", relativepath) 
                    continue 
            cleaned_resources.append(r) 
            
        package['resources'] = cleaned_resources 
        repo.package = package 
        
        with open('datapackage.json', 'w') as fd: 
            fd.write(json.dumps(repo.package, indent=4))

        return {
            'status': 'success',
            'message': ''
        }