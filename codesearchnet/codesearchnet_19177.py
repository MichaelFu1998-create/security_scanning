def make_tokens_dir(dir_, sources):
    """Create a new directory named <dir_>. Create a new file within it called
    sources.json. The input <sources> is a list of names of tokenized texts.
    Write <sources> into sources.json.
    """
    os.mkdir(tokens_dir + dir_)
    for source in sources:
        if not os.path.isfile(corpora_dir + source):
            print('Invalid source: ' + source)
            return

    with open(tokens_dir + dir_ + '/sources.json', 'w') as outjson:
        json.dump(sources, outjson)