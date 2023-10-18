def multi_run_epicom(graphs: Iterable[BELGraph], path: Union[None, str, TextIO]) -> None:
    """Run EpiCom analysis on many graphs."""
    if isinstance(path, str):
        with open(path, 'w') as file:
            _multi_run_helper_file_wrapper(graphs, file)

    else:
        _multi_run_helper_file_wrapper(graphs, path)