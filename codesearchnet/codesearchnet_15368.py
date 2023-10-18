def heatmap(genes_by_samples_matrix, sample_attributes, title='Axial Heatmap', scripts_mode="CDN", data_mode="directory",
            organism="human", separate_zscore_by=["system"],
            output_dir=".", filename="heatmap.html", version=this_version):
    """
    Arguments:
        genes_by_samples_matrix (pandas.DataFrame): dataframe indexed by genes, columns are samples
        sample_attributes (pandas.DataFrame): dataframe indexed by samples, columns are sample attributes (e.g. classes)
        title (str): The title of the plot (to be embedded in the html).
        scripts_mode (str): Choose from [`"CDN"`, `"directory"`, `"inline"`]:

            - `"CDN"` compiles a single HTML page with links to scripts hosted on a CDN,

            - `"directory"` compiles a directory with all scripts locally cached,

            - `"inline"` compiles a single HTML file with all scripts/styles inlined.

        data_mode (str): Choose from ["directory", "inline"]:

            - "directory" compiles a directory with all data locally cached,

            - "inline" compiles a single HTML file with all data inlined.

        organism (str): `"human"` or `"mouse"`
        separate_zscore_by (list):
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

    _verify_sample_by_genes_matrix(genes_by_samples_matrix)
    _verify_sample_attributes(genes_by_samples_matrix, sample_attributes)
    genes_by_samples_matrix = genes_by_samples_matrix.round(2)
    # TODO drop all zero rows

    matrix = f"var matrix = {genes_by_samples_matrix.to_json(orient='columns')};"
    classes = f"var classes = {sample_attributes.to_json(orient='index')};"

    data_block = _data_block(data_mode, [('matrix', matrix), ('classes', classes)], output_dir, organism=organism)

    # Scripts =======================

    scripts = third_party_scripts + [CDN_url(version)+"js/util.js", CDN_url(version)+"js/reorder.js", CDN_url(version)+"js/heatmap.js"]

    scripts_block = _scripts_block(scripts, scripts_mode, output_dir)


    html = templateEnv.get_template('heatmap.html.j2').render(title=title, scripts_block=scripts_block+'\n'+data_block, separate_zscore_by=separate_zscore_by)

    (output_dir / filename).write_text(html)


    return (output_dir / filename).resolve()