def belns(keyword: str, file: TextIO, encoding: Optional[str], use_names: bool):
    """Write as a BEL namespace."""
    directory = get_data_dir(keyword)
    obo_url = f'http://purl.obolibrary.org/obo/{keyword}.obo'
    obo_path = os.path.join(directory, f'{keyword}.obo')
    obo_cache_path = os.path.join(directory, f'{keyword}.obo.pickle')

    obo_getter = make_obo_getter(obo_url, obo_path, preparsed_path=obo_cache_path)
    graph = obo_getter()
    convert_obo_graph_to_belns(
        graph,
        file=file,
        encoding=encoding,
        use_names=use_names,
    )