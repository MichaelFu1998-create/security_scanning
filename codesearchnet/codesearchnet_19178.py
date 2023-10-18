def make_tokens_list(dir_, filters):
    """Find sources.json in <dir_>. It contains a list of tokenized texts. For
    each tokenized text listed in sources.json, read its tokens, filter them,
    and add them to an aggregated list. Write the aggregated list to disk using
    a filename based on the <filters> given.
    """
    with open(tokens_dir + dir_ + '/sources.json', 'r') as injson:
        data = json.load(injson)
        sources = [corpora_dir + fname for fname in data]

    with open('data/skipwords.txt', 'r') as f:
        skipwords = [line.rstrip() for line in f]

    tokens_list = []
    for fname in sources:
        print("Incorporating tokens from " + fname)
        with open(fname, 'r') as injson:
            data = json.load(injson)
            words = [w.lower() for w in data if not w == '']
            filtered = [w for w,p in nltk.pos_tag(words) if p in filters]
            sanitized = [w for w in filtered if not w in skipwords]
            tokens_list += sanitized

    tokens_list = list(set(tokens_list)) # unique
    target = tokens_dir + dir_ + '/' + '-'.join(filters) + '.json'
    with open(target, 'w') as outjson:
        json.dump(tokens_list, outjson)