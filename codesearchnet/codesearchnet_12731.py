def _check_hla_alleles(
            alleles,
            valid_alleles=None):
        """
        Given a list of HLA alleles and an optional list of valid
        HLA alleles, return a set of alleles that we will pass into
        the MHC binding predictor.
        """
        require_iterable_of(alleles, string_types, "HLA alleles")

        # Don't run the MHC predictor twice for homozygous alleles,
        # only run it for unique alleles
        alleles = {
            normalize_allele_name(allele.strip().upper())
            for allele in alleles
        }
        if valid_alleles:
            # For some reason netMHCpan drops the '*' in names, so
            # 'HLA-A*03:01' becomes 'HLA-A03:01'
            missing_alleles = [
                allele
                for allele in alleles
                if allele not in valid_alleles
            ]
            if len(missing_alleles) > 0:
                raise UnsupportedAllele(
                    "Unsupported HLA alleles: %s" % missing_alleles)

        return list(alleles)