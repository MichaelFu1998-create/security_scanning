def get_difference_model(self, category):
        """
        Get the equation corresponding to a variation wrt category. For example
        if::

            modelstr = {
                'full' :'H(I) + B',
                'dH' : 'dH(I)',
                'dI' : 'H(dI)',
                'dB' : 'dB'
            }

            varmap = {'H': 'psf', 'I': 'obj', 'B': 'bkg'}

        then ``get_difference_model('obj') == modelstr['dI'] == 'H(dI)'``
        """
        name = self.diffname(self.ivarmap[category])
        return self.modelstr.get(name)