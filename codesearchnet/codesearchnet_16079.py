def gc_content(self, as_decimal=True):
        """Returns the GC content for the sequence.
        Notes:
            This method ignores N when calculating the length of the sequence.
            It does not, however ignore other ambiguous bases. It also only
            includes the ambiguous base S (G or C). In this sense the method is
            conservative with its calculation.

        Args:
            as_decimal (bool): Return the result as a decimal. Setting to False
            will return as a percentage. i.e for the sequence GCAT it will
            return 0.5 by default and 50.00 if set to False.

        Returns:
            float: GC content calculated as the number of G, C, and S divided
            by the number of (non-N) bases (length).

        """
        gc_total = 0.0
        num_bases = 0.0
        n_tuple = tuple('nN')
        accepted_bases = tuple('cCgGsS')

        # counter sums all unique characters in sequence. Case insensitive.
        for base, count in Counter(self.seq).items():

            # dont count N in the number of bases
            if base not in n_tuple:
                num_bases += count

                if base in accepted_bases:  # S is a G or C
                    gc_total += count

        gc_content = gc_total / num_bases

        if not as_decimal:  # return as percentage
            gc_content *= 100

        return gc_content