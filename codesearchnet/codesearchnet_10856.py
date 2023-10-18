def zplane(self,auto_scale=True,size=2,detect_mult=True,tol=0.001):
        """
        Plot the poles and zeros of the FIR filter in the z-plane
        """
        ssd.zplane(self.b,[1],auto_scale,size,tol)