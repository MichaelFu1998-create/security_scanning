def visit_BitVecConcat(self, expression, *operands):
        """ concat( extract(k1, 0, a), extract(sizeof(a)-k1, k1, a))  ==> a
            concat( extract(k1, beg, a), extract(end, k1, a))  ==> extract(beg, end, a)
        """
        op = expression.operands[0]

        value = None
        end = None
        begining = None
        for o in operands:
            # If found a non BitVecExtract, do not apply
            if not isinstance(o, BitVecExtract):
                return None
            # Set the value for the first item
            if value is None:
                value = o.value
                begining = o.begining
                end = o.end
            else:
                # If concat of extracts of different values do not apply
                if value is not o.value:
                    return None
                # If concat of non contiguous extracs do not apply
                if begining != o.end + 1:
                    return None
                # update begining variable
                begining = o.begining

        if value is not None:
            if end + 1 == value.size and begining == 0:
                return value
            else:
                return BitVecExtract(value, begining, end - begining + 1, taint=expression.taint)