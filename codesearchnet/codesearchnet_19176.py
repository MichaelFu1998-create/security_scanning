def tokenize_texts():
    """Generate a json file for each txt file in the /data/corpora directory."""
    text_files = [fname for fname in os.listdir(corpora_dir) \
        if fname.split('.')[1] == 'txt']

    for text_fname in text_files:
        json_fname = text_fname.split('.')[0] + '.json'
        if os.path.isfile(corpora_dir + json_fname):
            continue # already tokenized

        print("Tokenizing " + text_fname)
        text = open(corpora_dir + text_fname).read()
        words = nltk.word_tokenize(text)
        with open(corpora_dir + json_fname, 'w') as outjson:
            json.dump(words, outjson)