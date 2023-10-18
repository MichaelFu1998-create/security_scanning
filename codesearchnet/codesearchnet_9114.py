def name(self):
        """ The instruction name/mnemonic """
        if self._name == 'PUSH':
            return 'PUSH%d' % self.operand_size
        elif self._name == 'DUP':
            return 'DUP%d' % self.pops
        elif self._name == 'SWAP':
            return 'SWAP%d' % (self.pops - 1)
        elif self._name == 'LOG':
            return 'LOG%d' % (self.pops - 2)
        return self._name