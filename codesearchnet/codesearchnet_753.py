def basic_clean_str(string):
    """Tokenization/string cleaning for a datasets."""
    string = re.sub(r"\n", " ", string)  # '\n'      --> ' '
    string = re.sub(r"\'s", " \'s", string)  # it's      --> it 's
    string = re.sub(r"\’s", " \'s", string)
    string = re.sub(r"\'ve", " have", string)  # they've   --> they have
    string = re.sub(r"\’ve", " have", string)
    string = re.sub(r"\'t", " not", string)  # can't     --> can not
    string = re.sub(r"\’t", " not", string)
    string = re.sub(r"\'re", " are", string)  # they're   --> they are
    string = re.sub(r"\’re", " are", string)
    string = re.sub(r"\'d", "", string)  # I'd (I had, I would) --> I
    string = re.sub(r"\’d", "", string)
    string = re.sub(r"\'ll", " will", string)  # I'll      --> I will
    string = re.sub(r"\’ll", " will", string)
    string = re.sub(r"\“", "  ", string)  # “a”       --> “ a ”
    string = re.sub(r"\”", "  ", string)
    string = re.sub(r"\"", "  ", string)  # "a"       --> " a "
    string = re.sub(r"\'", "  ", string)  # they'     --> they '
    string = re.sub(r"\’", "  ", string)  # they’     --> they ’
    string = re.sub(r"\.", " . ", string)  # they.     --> they .
    string = re.sub(r"\,", " , ", string)  # they,     --> they ,
    string = re.sub(r"\!", " ! ", string)
    string = re.sub(r"\-", "  ", string)  # "low-cost"--> lost cost
    string = re.sub(r"\(", "  ", string)  # (they)    --> ( they)
    string = re.sub(r"\)", "  ", string)  # ( they)   --> ( they )
    string = re.sub(r"\]", "  ", string)  # they]     --> they ]
    string = re.sub(r"\[", "  ", string)  # they[     --> they [
    string = re.sub(r"\?", "  ", string)  # they?     --> they ?
    string = re.sub(r"\>", "  ", string)  # they>     --> they >
    string = re.sub(r"\<", "  ", string)  # they<     --> they <
    string = re.sub(r"\=", "  ", string)  # easier=   --> easier =
    string = re.sub(r"\;", "  ", string)  # easier;   --> easier ;
    string = re.sub(r"\;", "  ", string)
    string = re.sub(r"\:", "  ", string)  # easier:   --> easier :
    string = re.sub(r"\"", "  ", string)  # easier"   --> easier "
    string = re.sub(r"\$", "  ", string)  # $380      --> $ 380
    string = re.sub(r"\_", "  ", string)  # _100     --> _ 100
    string = re.sub(r"\s{2,}", " ", string)  # Akara is    handsome --> Akara is handsome
    return string.strip().lower()