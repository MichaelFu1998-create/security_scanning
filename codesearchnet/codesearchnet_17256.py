def _get_drug_target_interactions(manager: Optional['bio2bel_drugbank.manager'] = None) -> Mapping[str, List[str]]:
    """Get a mapping from drugs to their list of gene."""
    if manager is None:
        import bio2bel_drugbank
        manager = bio2bel_drugbank.Manager()

    if not manager.is_populated():
        manager.populate()

    return manager.get_drug_to_hgnc_symbols()