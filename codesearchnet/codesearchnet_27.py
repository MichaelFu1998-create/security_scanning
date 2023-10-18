def load_results(root_dir_or_dirs, enable_progress=True, enable_monitor=True, verbose=False):
    '''
    load summaries of runs from a list of directories (including subdirectories)
    Arguments:

    enable_progress: bool - if True, will attempt to load data from progress.csv files (data saved by logger). Default: True

    enable_monitor: bool - if True, will attempt to load data from monitor.csv files (data saved by Monitor environment wrapper). Default: True

    verbose: bool - if True, will print out list of directories from which the data is loaded. Default: False


    Returns:
    List of Result objects with the following fields:
         - dirname - path to the directory data was loaded from
         - metadata - run metadata (such as command-line arguments and anything else in metadata.json file
         - monitor - if enable_monitor is True, this field contains pandas dataframe with loaded monitor.csv file (or aggregate of all *.monitor.csv files in the directory)
         - progress - if enable_progress is True, this field contains pandas dataframe with loaded progress.csv file
    '''
    import re
    if isinstance(root_dir_or_dirs, str):
        rootdirs = [osp.expanduser(root_dir_or_dirs)]
    else:
        rootdirs = [osp.expanduser(d) for d in root_dir_or_dirs]
    allresults = []
    for rootdir in rootdirs:
        assert osp.exists(rootdir), "%s doesn't exist"%rootdir
        for dirname, dirs, files in os.walk(rootdir):
            if '-proc' in dirname:
                files[:] = []
                continue
            monitor_re = re.compile(r'(\d+\.)?(\d+\.)?monitor\.csv')
            if set(['metadata.json', 'monitor.json', 'progress.json', 'progress.csv']).intersection(files) or \
               any([f for f in files if monitor_re.match(f)]):  # also match monitor files like 0.1.monitor.csv
                # used to be uncommented, which means do not go deeper than current directory if any of the data files
                # are found
                # dirs[:] = []
                result = {'dirname' : dirname}
                if "metadata.json" in files:
                    with open(osp.join(dirname, "metadata.json"), "r") as fh:
                        result['metadata'] = json.load(fh)
                progjson = osp.join(dirname, "progress.json")
                progcsv = osp.join(dirname, "progress.csv")
                if enable_progress:
                    if osp.exists(progjson):
                        result['progress'] = pandas.DataFrame(read_json(progjson))
                    elif osp.exists(progcsv):
                        try:
                            result['progress'] = read_csv(progcsv)
                        except pandas.errors.EmptyDataError:
                            print('skipping progress file in ', dirname, 'empty data')
                    else:
                        if verbose: print('skipping %s: no progress file'%dirname)

                if enable_monitor:
                    try:
                        result['monitor'] = pandas.DataFrame(monitor.load_results(dirname))
                    except monitor.LoadMonitorResultsError:
                        print('skipping %s: no monitor files'%dirname)
                    except Exception as e:
                        print('exception loading monitor file in %s: %s'%(dirname, e))

                if result.get('monitor') is not None or result.get('progress') is not None:
                    allresults.append(Result(**result))
                    if verbose:
                        print('successfully loaded %s'%dirname)

    if verbose: print('loaded %i results'%len(allresults))
    return allresults