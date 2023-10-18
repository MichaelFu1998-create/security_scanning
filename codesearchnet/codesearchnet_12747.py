def _prepare_drb_allele_name(self, parsed_beta_allele):
        """
        Assume that we're dealing with a human DRB allele
        which NetMHCIIpan treats differently because there is
        little population diversity in the DR-alpha gene
        """
        if "DRB" not in parsed_beta_allele.gene:
            raise ValueError("Unexpected allele %s" % parsed_beta_allele)
        return "%s_%s%s" % (
            parsed_beta_allele.gene,
            parsed_beta_allele.allele_family,
            parsed_beta_allele.allele_code)