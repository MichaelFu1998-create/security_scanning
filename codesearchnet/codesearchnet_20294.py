def get_diffs(history):
    """
    Look at files and compute the diffs intelligently
    """

    # First get all possible representations
    mgr = plugins_get_mgr() 
    keys = mgr.search('representation')['representation']
    representations = [mgr.get_by_key('representation', k) for k in keys]

    for i in range(len(history)):
        if i+1 > len(history) - 1:
            continue

        prev = history[i]
        curr = history[i+1]

        #print(prev['subject'], "==>", curr['subject'])
        #print(curr['changes'])
        for c in curr['changes']:
            
            path = c['path']

            # Skip the metadata file
            if c['path'].endswith('datapackage.json'): 
                continue 

            # Find a handler for this kind of file...
            handler = None 
            for r in representations: 
                if r.can_process(path): 
                    handler = r 
                    break 
            
            if handler is None: 
                continue 

            # print(path, "being handled by", handler)

            v1_hex = prev['commit']
            v2_hex = curr['commit']

            temp1 = tempfile.mkdtemp(prefix="dgit-diff-") 
            
            try: 
                for h in [v1_hex, v2_hex]: 
                    filename = '{}/{}/checkout.tar'.format(temp1, h)
                    try:
                        os.makedirs(os.path.dirname(filename))
                    except:
                        pass 
                    extractcmd = ['git', 'archive', '-o', filename, h, path]
                    output = run(extractcmd)
                    if 'fatal' in output: 
                        raise Exception("File not present in commit") 
                    with cd(os.path.dirname(filename)): 
                        cmd = ['tar', 'xvf', 'checkout.tar']
                        output = run(cmd) 
                        if 'fatal' in output: 
                            print("Cleaning up - fatal 1", temp1)
                            shutil.rmtree(temp1)
                            continue 

                # Check to make sure that 
                path1 = os.path.join(temp1, v1_hex, path) 
                path2 = os.path.join(temp1, v2_hex, path) 
                if not os.path.exists(path1) or not os.path.exists(path2): 
                    # print("One of the two output files is missing") 
                    shutil.rmtree(temp1)
                    continue 

                #print(path1, path2) 

                # Now call the handler
                diff = handler.get_diff(path1, path2)

                # print("Inserting diff", diff)
                c['diff'] = diff

            except Exception as e: 
                #traceback.print_exc() 
                #print("Cleaning up - Exception ", temp1)
                shutil.rmtree(temp1)