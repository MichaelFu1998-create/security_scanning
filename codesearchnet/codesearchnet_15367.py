def volcano(differential_dfs, title='Axial Volcano Plot', scripts_mode="CDN", data_mode="directory",
            organism="human", q_value_column_name="q", log2FC_column_name="logFC",
            output_dir=".", filename="volcano.html", version=this_version):
    """
    Arguments:
        differential_dfs (dict or pandas.DataFrame): python dict of names to pandas dataframes, or a single dataframe, indexed by gene symbols which must have columns named log2FC and qval.
        title (str): The title of the plot (to be embedded in the html).
        scripts_mode (str): Choose from [`"CDN"`, `"directory"`, `"inline"`]:

            - `"CDN"` compiles a single HTML page with links to scripts hosted on a CDN,

            - `"directory"` compiles a directory with all scripts locally cached,

            - `"inline"` compiles a single HTML file with all scripts/styles inlined.

        data_mode (str): Choose from ["directory", "inline"]:

            - "directory" compiles a directory with all data locally cached,

            - "inline" compiles a single HTML file with all data inlined.

        organism (str): `"human"` or `"mouse"`
        q_value_column_name (str):
        log2FC_column_name (str):
        output_dir (str): the directory in which to output the file
        filename (str): the filename of the output file
        version (str): the version of the javascripts to use.
            Leave the default to pin the version, or choose "latest" to get updates,
            or choose part of the version string to get minor updates.
    Returns:
        Path: The filepath which the html was outputted to.
    """

    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)

    # Data   =======================

    if isinstance(differential_dfs, pd.DataFrame):
        differential_dfs = {'differential': differential_dfs}

    for name, df in differential_dfs.items():
        df = df[[q_value_column_name, log2FC_column_name]]
        df.columns = ['q', 'logFC']
        df = df.round(2)
        # TODO drop all zero rows
        _verify_differential_df(df)

        del differential_dfs[name]
        differential_dfs[_sanitize(name)] = df

    names_and_differentials = f"var names_and_differentials = { '{'+ ','.join([_quote(name)+': '+df.to_json(orient='index') for name, df in differential_dfs.items()]) +'}' };"

    data_block = _data_block(data_mode, [('names_and_differentials', names_and_differentials)], output_dir, include_gene_sets=False, organism=organism)

    # Scripts =======================

    scripts = third_party_scripts + [CDN_url(version)+"js/util.js", CDN_url(version)+"js/GOrilla.js", CDN_url(version)+"js/volcano.js"]

    scripts_block = _scripts_block(scripts, scripts_mode, output_dir)


    html = templateEnv.get_template('volcano.html.j2').render(title=title, scripts_block=scripts_block+'\n'+data_block, organism="HOMO_SAPIENS")

    (output_dir / filename).write_text(html)


    return (output_dir / filename).resolve()