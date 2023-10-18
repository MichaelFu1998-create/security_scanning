def get_converted_psd(self, sides):
        """This function returns the PSD in the **sides** format

        :param str sides: the PSD format in ['onesided', 'twosided', 'centerdc']
        :return: the expected PSD.

        .. doctest::

            from spectrum import *
            p = pcovar(marple_data, 15)
            centerdc_psd = p.get_converted_psd('centerdc')

        .. note:: this function does not change the object, in particular, it
            does not change the :attr:`psd` attribute. If you want to change
            the psd on the fly, change the attribute :attr:`sides`.

        """
        if sides == self.sides:
            #nothing to be done is sides = :attr:`sides
            return self.__psd

        if self.datatype == 'complex':
            assert sides != 'onesided', \
                "complex datatype so sides cannot be onesided."

        if self.sides == 'onesided':
            logging.debug('Current sides is onesided')
            if sides == 'twosided':
                logging.debug('--->Converting to twosided')
                # here we divide everything by 2 to get the twosided version
                #N = self.NFFT
                newpsd = numpy.concatenate((self.psd[0:-1]/2., list(reversed(self.psd[0:-1]/2.))))
                # so we need to multiply by 2 the 0 and FS/2 frequencies
                newpsd[-1] = self.psd[-1]
                newpsd[0] *= 2.
            elif sides == 'centerdc':
                # FIXME. this assumes data is even so PSD is stored as
                # P0 X1 X2 X3 P1
                logging.debug('--->Converting to centerdc')
                P0 = self.psd[0]
                P1 = self.psd[-1]
                newpsd = numpy.concatenate((self.psd[-1:0:-1]/2., self.psd[0:-1]/2.))
                # so we need to multiply by 2 the 0 and F2/2 frequencies
                #newpsd[-1] = P0 / 2
                newpsd[0] = P1
        elif self.sides == 'twosided':
            logging.debug('Current sides is twosided')
            if sides == 'onesided':
                # we assume that data is stored as X0,X1,X2,X3,XN
                # that is original data is even.
                logging.debug('Converting to onesided assuming ori data is even')
                midN = (len(self.psd)-2) / 2
                newpsd = numpy.array(self.psd[0:int(midN)+2]*2)
                newpsd[0] /= 2
                newpsd[-1] = self.psd[-1]
            elif sides == 'centerdc':
                newpsd = stools.twosided_2_centerdc(self.psd)
        elif self.sides == 'centerdc': # same as twosided to onesided
            logging.debug('Current sides is centerdc')
            if sides == 'onesided':
                logging.debug('--->Converting to onesided')
                midN = int(len(self.psd) / 2)
                P1 = self.psd[0]
                newpsd = numpy.append(self.psd[midN:]*2, P1)
            elif sides == 'twosided':
                newpsd = stools.centerdc_2_twosided(self.psd)
        else:
            raise ValueError("sides must be set to 'onesided', 'twosided' or 'centerdc'")

        return newpsd