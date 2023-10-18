def trellis_plot(self,fsize=(6,4)):
        """
        Plots a trellis diagram of the possible state transitions.

        Parameters
        ----------
        fsize : Plot size for matplotlib.

        Examples
        --------
        >>> import matplotlib.pyplot as plt
        >>> from sk_dsp_comm.fec_conv import fec_conv
        >>> cc = fec_conv()
        >>> cc.trellis_plot()
        >>> plt.show()
        """

        branches_from = self.branches
        plt.figure(figsize=fsize)

        plt.plot(0,0,'.')
        plt.axis([-0.01, 1.01, -(self.Nstates-1)-0.05, 0.05])
        for m in range(self.Nstates):
            if branches_from.input1[m] == 0:
                plt.plot([0, 1],[-branches_from.states1[m], -m],'b')
                plt.plot([0, 1],[-branches_from.states1[m], -m],'r.')
            if branches_from.input2[m] == 0:
                plt.plot([0, 1],[-branches_from.states2[m], -m],'b')
                plt.plot([0, 1],[-branches_from.states2[m], -m],'r.')
            if branches_from.input1[m] == 1:
                plt.plot([0, 1],[-branches_from.states1[m], -m],'g')
                plt.plot([0, 1],[-branches_from.states1[m], -m],'r.')
            if branches_from.input2[m] == 1:
                plt.plot([0, 1],[-branches_from.states2[m], -m],'g')
                plt.plot([0, 1],[-branches_from.states2[m], -m],'r.')
        #plt.grid()
        plt.xlabel('One Symbol Transition')
        plt.ylabel('-State Index')
        msg = 'Rate %s, K = %d Trellis' %(self.rate, int(np.ceil(np.log2(self.Nstates)+1)))
        plt.title(msg)