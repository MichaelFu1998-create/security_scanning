def visit_BitVecExtract(self, expression, *operands):
        """ extract(sizeof(a), 0)(a)  ==> a
            extract(16, 0)( concat(a,b,c,d) ) => concat(c, d)
            extract(m,M)(and/or/xor a b ) => and/or/xor((extract(m,M) a) (extract(m,M) a)
        """
        op = expression.operands[0]
        begining = expression.begining
        end = expression.end
        size = end - begining + 1

        # extract(sizeof(a), 0)(a)  ==> a
        if begining == 0 and end + 1 == op.size:
            return op
        elif isinstance(op, BitVecExtract):
            return BitVecExtract(op.value, op.begining + begining, size, taint=expression.taint)
        elif isinstance(op, BitVecConcat):
            new_operands = []
            bitcount = 0
            for item in reversed(op.operands):
                if begining >= item.size:
                    begining -= item.size
                else:
                    if bitcount < expression.size:
                        new_operands.append(item)
                    bitcount += item.size
            if begining != expression.begining:
                return BitVecExtract(BitVecConcat(sum([x.size for x in new_operands]), *reversed(new_operands)),
                                     begining, expression.size, taint=expression.taint)
        if isinstance(op, (BitVecAnd, BitVecOr, BitVecXor)):
            bitoperand_a, bitoperand_b = op.operands
            return op.__class__(BitVecExtract(bitoperand_a, begining, expression.size), BitVecExtract(bitoperand_b, begining, expression.size), taint=expression.taint)