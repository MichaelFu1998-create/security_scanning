def main(args_list=None):
    """
    Script to make pMHC binding predictions from amino acid sequences.

    Usage example:
        mhctools
            --sequence SFFPIQQQQQAAALLLI \
            --sequence SILQQQAQAQQAQAASSSC \
            --extract-subsequences \
            --mhc-predictor netmhc \
            --mhc-alleles HLA-A0201 H2-Db \
            --mhc-predictor netmhc \
            --output-csv epitope.csv
    """
    args = parse_args(args_list)
    binding_predictions = run_predictor(args)
    df = binding_predictions.to_dataframe()
    logger.info('\n%s', df)
    if args.output_csv:
        df.to_csv(args.output_csv, index=False)
        print("Wrote: %s" % args.output_csv)