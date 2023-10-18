def annotate_metadata_action(repo):
    """
    Update metadata with the action history 
    """
    package = repo.package    

    print("Including history of actions")
    with cd(repo.rootdir): 
        filename = ".dgit/log.json"        
        if os.path.exists(filename):             
            history = open(filename).readlines() 
            actions = []
            for a in history: 
                try: 
                    a = json.loads(a)
                    for x in ['code']: 
                        if x not in a or a[x] == None: 
                            a[x] = "..."
                    actions.append(a)
                except:
                    pass 
            package['actions'] = actions