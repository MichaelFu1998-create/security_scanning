def cb_active_plot(self,start_ms,stop_ms,line_color='b'):
        """
        Plot timing information of time spent in the callback. This is similar
        to what a logic analyzer provides when probing an interrupt.

        cb_active_plot( start_ms,stop_ms,line_color='b')
        
        """
        # Find bounding k values that contain the [start_ms,stop_ms]
        k_min_idx = np.nonzero(np.ravel(np.array(self.DSP_tic)*1000 < start_ms))[0]
        if len(k_min_idx) < 1:
            k_min = 0
        else:
            k_min = k_min_idx[-1]
        k_max_idx = np.nonzero(np.ravel(np.array(self.DSP_tic)*1000 > stop_ms))[0]
        if len(k_min_idx) < 1:
            k_max= len(self.DSP_tic)
        else:
            k_max = k_max_idx[0]
        for k in range(k_min,k_max):
            if k == 0:
                plt.plot([0,self.DSP_tic[k]*1000,self.DSP_tic[k]*1000,
                         self.DSP_toc[k]*1000,self.DSP_toc[k]*1000],
                        [0,0,1,1,0],'b')
            else:
                plt.plot([self.DSP_toc[k-1]*1000,self.DSP_tic[k]*1000,self.DSP_tic[k]*1000,
                          self.DSP_toc[k]*1000,self.DSP_toc[k]*1000],[0,0,1,1,0],'b')
        plt.plot([self.DSP_toc[k_max-1]*1000,stop_ms],[0,0],'b')
        
        plt.xlim([start_ms,stop_ms])
        plt.title(r'Time Spent in the callback')
        plt.ylabel(r'Timing')
        plt.xlabel(r'Time (ms)')
        plt.grid();