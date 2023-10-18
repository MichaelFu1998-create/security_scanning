def save_json(data):
    """ Save assembly and samples as json """

    ## data as dict
    #### skip _ipcluster because it's made new
    #### skip _headers because it's loaded new
    #### statsfiles save only keys
    #### samples save only keys
    datadict = OrderedDict([
        ("_version", data.__dict__["_version"]),
        ("_checkpoint", data.__dict__["_checkpoint"]),
        ("name", data.__dict__["name"]), 
        ("dirs", data.__dict__["dirs"]),
        ("paramsdict", data.__dict__["paramsdict"]),
        ("samples", data.__dict__["samples"].keys()),
        ("populations", data.__dict__["populations"]),
        ("database", data.__dict__["database"]),
        ("clust_database", data.__dict__["clust_database"]),        
        ("outfiles", data.__dict__["outfiles"]),
        ("barcodes", data.__dict__["barcodes"]),
        ("stats_files", data.__dict__["stats_files"]),
        ("_hackersonly", data.__dict__["_hackersonly"]),
        ])

    ## sample dict
    sampledict = OrderedDict([])
    for key, sample in data.samples.iteritems():
        sampledict[key] = sample._to_fulldict()

    ## json format it using cumstom Encoder class
    fulldumps = json.dumps({
        "assembly": datadict,
        "samples": sampledict
        },
        cls=Encoder,
        sort_keys=False, indent=4, separators=(",", ":"),
        )

    ## save to file
    assemblypath = os.path.join(data.dirs.project, data.name+".json")
    if not os.path.exists(data.dirs.project):
        os.mkdir(data.dirs.project)
    
    ## protect save from interruption
    done = 0
    while not done:
        try:
            with open(assemblypath, 'w') as jout:
                jout.write(fulldumps)
            done = 1
        except (KeyboardInterrupt, SystemExit): 
            print('.')
            continue