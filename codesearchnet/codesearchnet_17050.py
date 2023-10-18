def write_neurommsig_bel(file,
                         df: pd.DataFrame,
                         disease: str,
                         nift_values: Mapping[str, str],
                         ):
    """Writes the NeuroMMSigDB excel sheet to BEL

    :param file: a file or file-like that can be writen to
    :param df:
    :param disease:
    :param nift_values: a dictionary of lowercased to normal names in NIFT
    """
    write_neurommsig_biolerplate(disease, file)

    missing_features = set()
    fixed_caps = set()
    nift_value_originals = set(nift_values.values())

    graph = BELGraph(
        name=f'NeuroMMSigDB for {disease}',
        description=f'SNP and Clinical Features for Subgraphs in {disease}',
        authors='Daniel Domingo-Fernández, Charles Tapley Hoyt, Mufassra Naz, Aybuge Altay, Anandhi Iyappan',
        contact='daniel.domingo.fernandez@scai.fraunhofer.de',
        version=time.strftime('%Y%m%d'),
    )

    for pathway, pathway_df in df.groupby(pathway_column):
        sorted_pathway_df = pathway_df.sort_values(genes_column)
        sliced_df = sorted_pathway_df[columns].itertuples()

        for _, gene, pubmeds, lit_snps, gwas_snps, ld_block_snps, clinical_features, clinical_snps in sliced_df:
            gene = ensure_quotes(gene)

            for snp in itt.chain(lit_snps or [], gwas_snps or [], ld_block_snps or [], clinical_snps or []):
                if not snp.strip():
                    continue
                graph.add_association(
                    Gene('HGNC', gene),
                    Gene('DBSNP', snp),
                    evidence='Serialized from NeuroMMSigDB',
                    citation='28651363',
                    annotations={
                        'MeSHDisease': disease,
                    },
                )

            for clinical_feature in clinical_features or []:
                if not clinical_feature.strip():
                    continue

                if clinical_feature.lower() not in nift_values:
                    missing_features.add(clinical_feature)
                    continue

                if clinical_feature not in nift_value_originals:
                    fixed_caps.add((clinical_feature, nift_values[clinical_feature.lower()]))
                    clinical_feature = nift_values[clinical_feature.lower()]  # fix capitalization

                graph.add_association(
                    Gene('HGNC', gene),
                    Abundance('NIFT', clinical_feature),
                    evidence='Serialized from NeuroMMSigDB',
                    citation='28651363',
                    annotations={
                        'MeSHDisease': disease,
                    },
                )

                if clinical_snps:
                    for clinical_snp in clinical_snps:
                        graph.add_association(
                            Gene('DBSNP', clinical_snp),
                            Abundance('NIFT', clinical_feature),
                            evidence='Serialized from NeuroMMSigDB',
                            citation='28651363',
                            annotations={
                                'MeSHDisease': disease,
                            },
                        )

    if missing_features:
        log.warning('Missing Features in %s', disease)
        for feature in missing_features:
            log.warning(feature)

    if fixed_caps:
        log.warning('Fixed capitalization')
        for broken, fixed in fixed_caps:
            log.warning('%s -> %s', broken, fixed)