def prepare_allele_name(self, allele_name):
        """
        netMHCIIpan has some unique requirements for allele formats,
        expecting the following forms:
         - DRB1_0101 (for non-alpha/beta pairs)
         - HLA-DQA10501-DQB10636 (for alpha and beta pairs)

        Other than human class II alleles, the only other alleles that
        netMHCIIpan accepts are the following mouse alleles:
         - H-2-IAb
         - H-2-IAd
        """
        parsed_alleles = parse_classi_or_classii_allele_name(allele_name)
        if len(parsed_alleles) == 1:
            allele = parsed_alleles[0]
            if allele.species == "H-2":
                return "%s-%s%s" % (
                    allele.species,
                    allele.gene,
                    allele.allele_code)
            return self._prepare_drb_allele_name(allele)

        else:
            alpha, beta = parsed_alleles
            if "DRA" in alpha.gene:
                return self._prepare_drb_allele_name(beta)
            return "HLA-%s%s%s-%s%s%s" % (
                alpha.gene,
                alpha.allele_family,
                alpha.allele_code,
                beta.gene,
                beta.allele_family,
                beta.allele_code)