def lexsort(self, *order):
        """
        The lexical sort order is specified by a list of string
        arguments. Each string is a key name prefixed by '+' or '-'
        for ascending and descending sort respectively. If the key is
        not found in the operand's set of varying keys, it is ignored.
        """
        if order == []:
            raise Exception("Please specify the keys for sorting, use"
                            "'+' prefix for ascending,"
                            "'-' for descending.)")

        if not set(el[1:] for el in order).issubset(set(self.varying_keys)):
            raise Exception("Key(s) specified not in the set of varying keys.")

        sorted_args = copy.deepcopy(self)
        specs_param = sorted_args.params('specs')
        specs_param.constant = False
        sorted_args.specs = self._lexsorted_specs(order)
        specs_param.constant = True
        sorted_args._lexorder = order
        return sorted_args