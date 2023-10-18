def kernel_gaussian(self, sizeMS, sigmaMS=None, forwardOnly=False):
        """create kernel based on this ABF info."""
        sigmaMS=sizeMS/10 if sigmaMS is None else sigmaMS
        size,sigma=sizeMS*self.pointsPerMs,sigmaMS*self.pointsPerMs
        self.kernel=swhlab.common.kernel_gaussian(size,sigma,forwardOnly)
        return self.kernel