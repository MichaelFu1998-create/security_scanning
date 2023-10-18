def PALIGNR(cpu, dest, src, offset):
        """ALIGNR concatenates the destination operand (the first operand) and the source
            operand (the second operand) into an intermediate composite, shifts the composite
            at byte granularity to the right by a constant immediate, and extracts the right-
            aligned result into the destination."""
        dest.write(
            Operators.EXTRACT(
                Operators.CONCAT(dest.size * 2, dest.read(), src.read()),
                offset.read() * 8,
                dest.size))