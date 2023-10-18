def main():
    """Convert the Alzheimer's and Parkinson's disease NeuroMMSig excel sheets to BEL."""
    logging.basicConfig(level=logging.INFO)
    log.setLevel(logging.INFO)

    bms_base = get_bms_base()
    neurommsig_base = get_neurommsig_base()
    neurommsig_excel_dir = os.path.join(neurommsig_base, 'resources', 'excels', 'neurommsig')

    nift_values = get_nift_values()

    log.info('Starting Alzheimers')

    ad_path = os.path.join(neurommsig_excel_dir, 'alzheimers', 'alzheimers.xlsx')
    ad_df = preprocess(ad_path)
    with open(os.path.join(bms_base, 'aetionomy', 'alzheimers', 'neurommsigdb_ad.bel'), 'w') as ad_file:
        write_neurommsig_bel(ad_file, ad_df, mesh_alzheimer, nift_values)

    log.info('Starting Parkinsons')

    pd_path = os.path.join(neurommsig_excel_dir, 'parkinsons', 'parkinsons.xlsx')
    pd_df = preprocess(pd_path)
    with open(os.path.join(bms_base, 'aetionomy', 'parkinsons', 'neurommsigdb_pd.bel'), 'w') as pd_file:
        write_neurommsig_bel(pd_file, pd_df, mesh_parkinson, nift_values)