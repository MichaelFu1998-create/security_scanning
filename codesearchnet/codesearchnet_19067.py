def generate(grammar=None, num=1, output=sys.stdout, max_recursion=10, seed=None):
    """Load and generate ``num`` number of top-level rules from the specified grammar.

    :param list grammar: The grammar file to load and generate data from
    :param int num: The number of times to generate data
    :param output: The output destination (an open, writable stream-type object. default=``sys.stdout``)
    :param int max_recursion: The maximum reference-recursion when generating data (default=``10``)
    :param int seed: The seed to initialize the PRNG with. If None, will not initialize it.
    """
    if seed is not None:
        gramfuzz.rand.seed(seed)

    fuzzer = gramfuzz.GramFuzzer()
    fuzzer.load_grammar(grammar)

    cat_group = os.path.basename(grammar).replace(".py", "")

    results = fuzzer.gen(cat_group=cat_group, num=num, max_recursion=max_recursion)
    for res in results:
        output.write(res)