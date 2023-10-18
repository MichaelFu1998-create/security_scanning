def eval(self, x, y, z):
        """Evaluate the function in (x, y, z).
        The function is rotationally symmetric around z.
        """
        ro = np.sqrt(x**2 + y**2)
        zs, xs = ro.shape
        v = self.eval_xz(ro.ravel(), z.ravel())
        return v.reshape(zs, xs)