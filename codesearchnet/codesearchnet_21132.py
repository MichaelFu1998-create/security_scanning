def get_pos(vcf_line):
        """
        Very lightweight parsing of a vcf line to get position.

        Returns a dict containing:
        'chrom': index of chromosome (int), indicates sort order
        'pos': position on chromosome (int)
        """
        if not vcf_line:
            return None
        vcf_data = vcf_line.strip().split('\t')
        return_data = dict()
        return_data['chrom'] = CHROM_INDEX[vcf_data[0]]
        return_data['pos'] = int(vcf_data[1])
        return return_data