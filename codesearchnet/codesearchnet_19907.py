def save(self,callit="misc",closeToo=True,fullpath=False):
        """save the existing figure. does not close it."""
        if fullpath is False:
            fname=self.abf.outPre+"plot_"+callit+".jpg"
        else:
            fname=callit
        if not os.path.exists(os.path.dirname(fname)):
            os.mkdir(os.path.dirname(fname))
        plt.savefig(fname)
        self.log.info("saved [%s]",os.path.basename(fname))
        if closeToo:
            plt.close()