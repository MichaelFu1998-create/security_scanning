def _parse_genotype(self, vcf_fields):
        """Parse genotype from VCF line data"""
        format_col = vcf_fields[8].split(':')
        genome_data = vcf_fields[9].split(':')
        try:
            gt_idx = format_col.index('GT')
        except ValueError:
            return []
        return [int(x) for x in re.split(r'[\|/]', genome_data[gt_idx]) if
                x != '.']