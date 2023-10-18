def LDREX(cpu, dest, src, offset=None):
        """
        LDREX loads data from memory.
        * If the physical address has the shared TLB attribute, LDREX
          tags the physical address as exclusive access for the current
          processor, and clears any exclusive access tag for this
          processor for any other physical address.
        * Otherwise, it tags the fact that the executing processor has
          an outstanding tagged physical address.

        :param Armv7Operand dest: the destination register; register
        :param Armv7Operand src: the source operand: register
        """
        # TODO: add lock mechanism to underlying memory --GR, 2017-06-06
        cpu._LDR(dest, src, 32, False, offset)